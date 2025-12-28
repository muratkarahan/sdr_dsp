#!/usr/bin/env python3
"""
Multi-Repository Traffic Monitor
Fetches and displays traffic statistics for multiple GitHub repositories.

Usage:
    python fetch_all_repos_traffic.py <github_token> [username]

Arguments:
    github_token: GitHub personal access token with repo scope
    username: GitHub username (optional, defaults to authenticated user)

Example:
    python fetch_all_repos_traffic.py ghp_xxxxxxxxxxxx muratkarahan
"""

import sys
import json
from datetime import datetime
import requests


def get_user_repositories(token, username=None):
    """
    Fetch all repositories for a user.
    
    Args:
        token: GitHub API token
        username: GitHub username (optional)
    
    Returns:
        List of repository objects
    """
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    if username:
        url = f'https://api.github.com/users/{username}/repos'
    else:
        url = 'https://api.github.com/user/repos'
    
    repos = []
    page = 1
    
    while True:
        try:
            response = requests.get(url, headers=headers, params={'page': page, 'per_page': 100})
            response.raise_for_status()
            data = response.json()
            
            if not data:
                break
            
            repos.extend(data)
            page += 1
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repositories: {e}", file=sys.stderr)
            break
    
    return repos


def get_traffic_data(repo_full_name, token):
    """
    Fetch traffic data for a repository.
    
    Args:
        repo_full_name: Full repository name (owner/repo)
        token: GitHub API token
    
    Returns:
        Dictionary containing traffic data
    """
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    base_url = f'https://api.github.com/repos/{repo_full_name}'
    
    traffic_data = {}
    
    # Fetch views
    try:
        response = requests.get(f'{base_url}/traffic/views', headers=headers)
        response.raise_for_status()
        traffic_data['views'] = response.json()
    except requests.exceptions.RequestException:
        traffic_data['views'] = {'count': 0, 'uniques': 0}
    
    # Fetch clones
    try:
        response = requests.get(f'{base_url}/traffic/clones', headers=headers)
        response.raise_for_status()
        traffic_data['clones'] = response.json()
    except requests.exceptions.RequestException:
        traffic_data['clones'] = {'count': 0, 'uniques': 0}
    
    return traffic_data


def display_traffic_summary(repos_traffic):
    """
    Display traffic summary for all repositories.
    
    Args:
        repos_traffic: List of tuples (repo_name, traffic_data)
    """
    print("=" * 80)
    print("TRAFFIC STATISTICS FOR ALL REPOSITORIES")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 80)
    print()
    
    # Sort repositories by total views
    repos_traffic.sort(key=lambda x: x[1]['views'].get('count', 0), reverse=True)
    
    total_views = 0
    total_unique_views = 0
    total_clones = 0
    total_unique_clones = 0
    
    print(f"{'Repository':<40} {'Views':<15} {'Clones':<15}")
    print("-" * 80)
    
    for repo_name, traffic in repos_traffic:
        views = traffic['views'].get('count', 0)
        unique_views = traffic['views'].get('uniques', 0)
        clones = traffic['clones'].get('count', 0)
        unique_clones = traffic['clones'].get('uniques', 0)
        
        total_views += views
        total_unique_views += unique_views
        total_clones += clones
        total_unique_clones += unique_clones
        
        views_str = f"{views} ({unique_views} unique)"
        clones_str = f"{clones} ({unique_clones} unique)"
        
        print(f"{repo_name:<40} {views_str:<15} {clones_str:<15}")
    
    print("-" * 80)
    print(f"{'TOTAL':<40} {f'{total_views} ({total_unique_views} unique)':<15} {f'{total_clones} ({total_unique_clones} unique)':<15}")
    print("=" * 80)
    print()
    print(f"📊 Total Repositories: {len(repos_traffic)}")
    print(f"👁️  Total Views: {total_views} (Unique: {total_unique_views})")
    print(f"📥 Total Clones: {total_clones} (Unique: {total_unique_clones})")
    print("=" * 80)


def main():
    """Main function to fetch and display traffic for all repositories."""
    if len(sys.argv) < 2:
        print("Usage: python fetch_all_repos_traffic.py <github_token> [username]")
        print()
        print("Arguments:")
        print("  github_token: GitHub personal access token with repo scope")
        print("  username: GitHub username (optional, defaults to authenticated user)")
        print()
        print("Example:")
        print("  python fetch_all_repos_traffic.py ghp_xxxxxxxxxxxx muratkarahan")
        sys.exit(1)
    
    token = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"Fetching repositories for {username if username else 'authenticated user'}...")
    repos = get_user_repositories(token, username)
    
    if not repos:
        print("No repositories found.")
        sys.exit(0)
    
    print(f"Found {len(repos)} repositories. Fetching traffic data...")
    print()
    
    repos_traffic = []
    for repo in repos:
        repo_name = repo['full_name']
        print(f"  Fetching traffic for {repo_name}...")
        traffic = get_traffic_data(repo_name, token)
        repos_traffic.append((repo_name, traffic))
    
    print()
    display_traffic_summary(repos_traffic)
    
    # Save to JSON file
    output_file = f"all_repos_traffic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(repos_traffic, f, indent=2)
    
    print()
    print(f"✅ Detailed traffic data saved to {output_file}")


if __name__ == '__main__':
    main()
