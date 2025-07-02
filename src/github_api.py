"""
GitHub API client for fetching user statistics and repository data
Handles GraphQL queries and rate limiting
"""

import os
import requests
from typing import Dict, Any, List, Tuple
from datetime import datetime


class GitHubAPI:
    """GitHub GraphQL API client"""
    
    def __init__(self):
        """Initialize GitHub API client"""
        self.access_token = os.environ.get('ACCESS_TOKEN')
        self.username = os.environ.get('USER_NAME', 'lelborn')
        
        if not self.access_token:
            raise ValueError("ACCESS_TOKEN environment variable is required")
        
        self.headers = {
            'authorization': f'token {self.access_token}',
            'content-type': 'application/json'
        }
        
        self.base_url = 'https://api.github.com/graphql'
        self.query_count = {
            'user_getter': 0,
            'follower_getter': 0,
            'graph_repos_stars': 0,
            'recursive_loc': 0,
            'graph_commits': 0,
            'loc_query': 0
        }
    
    def _make_request(self, query: str, variables: Dict[str, Any], operation_name: str) -> Dict[str, Any]:
        """Make GraphQL request to GitHub API"""
        self.query_count[operation_name] += 1
        
        payload = {
            'query': query,
            'variables': variables
        }
        
        response = requests.post(self.base_url, json=payload, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"{operation_name} failed with status {response.status_code}: {response.text}")
    
    def get_user_info(self) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """Get comprehensive user information"""
        query = '''
        query($login: String!){
            user(login: $login) {
                id
                createdAt
                location
                websiteUrl
                email
                twitterUsername
                bio
                company
                isHireable
            }
        }'''
        
        variables = {'login': self.username}
        result = self._make_request(query, variables, 'user_getter')
        
        user_data = result['data']['user']
        user_info = {
            'id': user_data['id'],
            'created_at': user_data['createdAt'],
            'location': user_data.get('location'),
            'website': user_data.get('websiteUrl'),
            'email': user_data.get('email'),
            'twitter': user_data.get('twitterUsername'),
            'bio': user_data.get('bio'),
            'company': user_data.get('company'),
            'is_hireable': user_data.get('isHireable', False)
        }
        
        return {'id': user_data['id']}, user_info
    
    def get_follower_count(self) -> int:
        """Get user's follower count"""
        query = '''
        query($login: String!){
            user(login: $login) {
                followers {
                    totalCount
                }
            }
        }'''
        
        variables = {'login': self.username}
        result = self._make_request(query, variables, 'follower_getter')
        
        return result['data']['user']['followers']['totalCount']
    
    def get_repository_stats(self, count_type: str, owner_affiliation: List[str], cursor: str = None) -> int:
        """Get repository statistics (count, stars, etc.)"""
        if count_type == 'repos':
            # For repository count, we can use the totalCount directly
            query = '''
            query ($owner_affiliation: [RepositoryAffiliation], $login: String!, $cursor: String) {
                user(login: $login) {
                    repositories(first: 100, after: $cursor, ownerAffiliations: $owner_affiliation) {
                        totalCount
                        pageInfo {
                            endCursor
                            hasNextPage
                        }
                    }
                }
            }'''
            
            variables = {
                'owner_affiliation': owner_affiliation,
                'login': self.username,
                'cursor': cursor
            }
            
            result = self._make_request(query, variables, 'graph_repos_stars')
            data = result['data']['user']['repositories']
            return data['totalCount']
            
        elif count_type == 'stars':
            # For star counting, we need to iterate through all repositories
            return self._get_total_stars(owner_affiliation)
    
    def _get_total_stars(self, owner_affiliation: List[str]) -> int:
        """Get total stars across all repositories with pagination"""
        total_stars = 0
        cursor = None
        
        while True:
            query = '''
            query ($owner_affiliation: [RepositoryAffiliation], $login: String!, $cursor: String) {
                user(login: $login) {
                    repositories(first: 100, after: $cursor, ownerAffiliations: $owner_affiliation) {
                        edges {
                            node {
                                ... on Repository {
                                    nameWithOwner
                                    stargazers {
                                        totalCount
                                    }
                                }
                            }
                        }
                        pageInfo {
                            endCursor
                            hasNextPage
                        }
                    }
                }
            }'''
            
            variables = {
                'owner_affiliation': owner_affiliation,
                'login': self.username,
                'cursor': cursor
            }
            
            result = self._make_request(query, variables, 'graph_repos_stars')
            data = result['data']['user']['repositories']
            
            # Count stars from this batch
            total_stars += self._count_stars(data['edges'])
            
            if not data['pageInfo']['hasNextPage']:
                break
                
            cursor = data['pageInfo']['endCursor']
        
        return total_stars
    
    def _count_stars(self, edges: List[Dict[str, Any]]) -> int:
        """Count total stars from repository edges"""
        total_stars = 0
        for edge in edges:
            total_stars += edge['node']['stargazers']['totalCount']
        return total_stars
    
    def get_commit_stats(self, start_date: str, end_date: str) -> int:
        """Get commit count for a date range"""
        query = '''
        query($start_date: DateTime!, $end_date: DateTime!, $login: String!) {
            user(login: $login) {
                contributionsCollection(from: $start_date, to: $end_date) {
                    contributionCalendar {
                        totalContributions
                    }
                }
            }
        }'''
        
        variables = {
            'start_date': start_date,
            'end_date': end_date,
            'login': self.username
        }
        
        result = self._make_request(query, variables, 'graph_commits')
        return result['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions']
    
    def get_lines_of_code(self, owner_affiliation: List[str], comment_size: int = 0, 
                         force_cache: bool = False, cursor: str = None, edges: List = None) -> List[int]:
        """Get lines of code statistics for repositories"""
        if edges is None:
            # Get all repositories first
            edges = self._get_all_repository_edges(owner_affiliation)
        
        total_added = 0
        total_deleted = 0
        total_commits = 0
        
        # Process repositories in batches to avoid rate limiting
        batch_size = 10
        for i in range(0, len(edges), batch_size):
            batch = edges[i:i + batch_size]
            for edge in batch:
                repo_name = edge['node']['nameWithOwner']
                try:
                    # Get commit statistics for this repository
                    repo_stats = self._get_repository_commit_stats(repo_name)
                    total_added += repo_stats['additions']
                    total_deleted += repo_stats['deletions']
                    total_commits += repo_stats['commits']
                except Exception as e:
                    print(f"⚠️  Warning: Could not fetch stats for {repo_name}: {e}")
                    continue
        
        total_loc = total_added - total_deleted
        return [total_added, total_deleted, total_loc, total_commits, False]
    
    def _get_all_repository_edges(self, owner_affiliation: List[str]) -> List[Dict[str, Any]]:
        """Get all repository edges for the user"""
        all_edges = []
        cursor = None
        
        while True:
            query = '''
            query ($owner_affiliation: [RepositoryAffiliation], $login: String!, $cursor: String) {
                user(login: $login) {
                    repositories(first: 100, after: $cursor, ownerAffiliations: $owner_affiliation) {
                        edges {
                            node {
                                ... on Repository {
                                    nameWithOwner
                                    isFork
                                    isArchived
                                }
                            }
                        }
                        pageInfo {
                            endCursor
                            hasNextPage
                        }
                    }
                }
            }'''
            
            variables = {
                'owner_affiliation': owner_affiliation,
                'login': self.username,
                'cursor': cursor
            }
            
            result = self._make_request(query, variables, 'recursive_loc')
            data = result['data']['user']['repositories']
            
            # Filter out forks and archived repositories
            filtered_edges = [
                edge for edge in data['edges'] 
                if not edge['node']['isFork'] and not edge['node']['isArchived']
            ]
            all_edges.extend(filtered_edges)
            
            if not data['pageInfo']['hasNextPage']:
                break
                
            cursor = data['pageInfo']['endCursor']
        
        return all_edges
    
    def _get_repository_commit_stats(self, repo_name: str) -> Dict[str, int]:
        """Get commit statistics for a specific repository"""
        # Use GitHub REST API for commit statistics
        rest_url = f"https://api.github.com/repos/{repo_name}/stats/participation"
        
        response = requests.get(rest_url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to get stats for {repo_name}: {response.status_code}")
        
        data = response.json()
        
        # Calculate totals from weekly data
        total_additions = 0
        total_deletions = 0
        total_commits = 0
        
        # Get detailed commit stats for the last year
        commits_url = f"https://api.github.com/repos/{repo_name}/commits"
        commits_response = requests.get(commits_url, headers=self.headers, params={'per_page': 100})
        
        if commits_response.status_code == 200:
            commits_data = commits_response.json()
            for commit in commits_data:
                # Get detailed commit info
                commit_sha = commit['sha']
                commit_detail_url = f"https://api.github.com/repos/{repo_name}/commits/{commit_sha}"
                commit_response = requests.get(commit_detail_url, headers=self.headers)
                
                if commit_response.status_code == 200:
                    commit_detail = commit_response.json()
                    if 'stats' in commit_detail:
                        total_additions += commit_detail['stats'].get('additions', 0)
                        total_deletions += commit_detail['stats'].get('deletions', 0)
                        total_commits += 1
        
        return {
            'additions': total_additions,
            'deletions': total_deletions,
            'commits': total_commits
        }
    
    def get_query_stats(self) -> Dict[str, int]:
        """Get query count statistics"""
        return self.query_count.copy()
    
    def get_total_queries(self) -> int:
        """Get total number of API queries made"""
        return sum(self.query_count.values())


# Global GitHub API instance (lazy initialization)
_github_api_instance = None

def get_github_api():
    """Get or create GitHub API instance"""
    global _github_api_instance
    if _github_api_instance is None:
        _github_api_instance = GitHubAPI()
    return _github_api_instance 