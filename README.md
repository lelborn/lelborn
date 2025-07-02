# Hi there, I'm Lewis Elborn 👋

<a href="https://github.com/lelborn">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/lelborn/lelborn/main/profile-dark.svg">
    <img alt="Lewis Elborn's GitHub Profile README" src="https://raw.githubusercontent.com/lelborn/lelborn/main/profile-light.svg">
  </picture>
</a>

*This profile is automatically generated and updated daily using GitHub Actions...*

## 🚀 About This Repository

This is my GitHub profile repository that automatically generates a dynamic README with real-time statistics from my GitHub activity. The profile showcases:

- **Real-time GitHub stats** (stars, repositories, followers, commits)
- **Lines of code** contributed across all repositories
- **Environment information** (OS, editor, etc.)
- **Personal information** with automatic age calculation

### 🏗️ Architecture

The project is built with a modular Python architecture:

```
src/
├── __init__.py          # Package exports and version info
├── config.py            # Configuration management
├── github_api.py        # GitHub API integration
├── svg_generator.py     # SVG file generation and updates
├── utils.py             # Core utility functions
├── file_ops.py          # File operations utilities
└── system_detection.py  # System and environment detection
```

### 🔧 Key Features

- **Modular Design**: Clean separation of concerns with dedicated modules
- **Performance Monitoring**: Built-in performance tracking for API calls
- **Error Handling**: Robust error handling and graceful degradation
- **Automated Updates**: GitHub Actions workflow for daily updates
- **Cross-platform**: Works on macOS, Windows, and Linux

### 📊 What Gets Updated

- Repository statistics (stars, repos, contributions)
- Follower count
- Lines of code metrics
- Commit statistics
- Environment information
- Build timestamps

The profile updates automatically every day at 4:00 AM UTC via GitHub Actions.
