#!/usr/bin/env python3
"""
GitHub Repository Traffic Monitor
Fetches and displays traffic statistics for the repository.
"""

import os
import sys
import json
from datetime import datetime
import requests


def get_traffic_data(repo_owner, repo_name, token):
    """
    Fetch traffic data from GitHub API.
    
    Args:
        repo_owner: Repository owner username
        repo_name: Repository name
        token: GitHub API token
    
    Returns:
        Dictionary containing traffic data
    """
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}'
    
    traffic_data = {}
    
    # Fetch views
    try:
        response = requests.get(f'{base_url}/traffic/views', headers=headers)
        response.raise_for_status()
        traffic_data['views'] = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching views: {e}", file=sys.stderr)
        traffic_data['views'] = None
    
    # Fetch clones
    try:
        response = requests.get(f'{base_url}/traffic/clones', headers=headers)
        response.raise_for_status()
        traffic_data['clones'] = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching clones: {e}", file=sys.stderr)
        traffic_data['clones'] = None
    
    # Fetch popular paths
    try:
        response = requests.get(f'{base_url}/traffic/popular/paths', headers=headers)
        response.raise_for_status()
        traffic_data['popular_paths'] = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching popular paths: {e}", file=sys.stderr)
        traffic_data['popular_paths'] = None
    
    # Fetch referrers
    try:
        response = requests.get(f'{base_url}/traffic/popular/referrers', headers=headers)
        response.raise_for_status()
        traffic_data['referrers'] = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching referrers: {e}", file=sys.stderr)
        traffic_data['referrers'] = None
    
    return traffic_data


def format_traffic_summary(repo_owner, repo_name, traffic_data):
    """
    Format traffic data into a readable summary.
    
    Args:
        repo_owner: Repository owner username
        repo_name: Repository name
        traffic_data: Dictionary containing traffic data
    
    Returns:
        Formatted string summary
    """
    summary = []
    summary.append("=" * 70)
    summary.append(f"Traffic Statistics for {repo_owner}/{repo_name}")
    summary.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    summary.append("=" * 70)
    summary.append("")
    
    # Views
    if traffic_data.get('views'):
        views = traffic_data['views']
        summary.append("📊 VIEWS (Last 14 days)")
        summary.append(f"  Total: {views.get('count', 0)}")
        summary.append(f"  Unique: {views.get('uniques', 0)}")
        summary.append("")
    
    # Clones
    if traffic_data.get('clones'):
        clones = traffic_data['clones']
        summary.append("📥 CLONES (Last 14 days)")
        summary.append(f"  Total: {clones.get('count', 0)}")
        summary.append(f"  Unique: {clones.get('uniques', 0)}")
        summary.append("")
    
    # Popular paths
    if traffic_data.get('popular_paths') and traffic_data['popular_paths']:
        summary.append("🔗 POPULAR PATHS")
        for i, path in enumerate(traffic_data['popular_paths'][:10], 1):
            summary.append(f"  {i}. {path['path']}")
            summary.append(f"     Views: {path['count']} (Unique: {path['uniques']})")
        summary.append("")
    
    # Referrers
    if traffic_data.get('referrers') and traffic_data['referrers']:
        summary.append("🌐 TOP REFERRERS")
        for i, referrer in enumerate(traffic_data['referrers'][:10], 1):
            summary.append(f"  {i}. {referrer['referrer']}")
            summary.append(f"     Views: {referrer['count']} (Unique: {referrer['uniques']})")
        summary.append("")
    
    summary.append("=" * 70)
    
    return "\n".join(summary)


def main():
    """Main function to fetch and display traffic statistics."""
    # Get repository information from environment
    github_repository = os.environ.get('GITHUB_REPOSITORY', '')
    github_token = os.environ.get('GITHUB_TOKEN', '')
    
    if not github_repository:
        print("Error: GITHUB_REPOSITORY environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    try:
        repo_owner, repo_name = github_repository.split('/')
    except ValueError:
        print(f"Error: Invalid GITHUB_REPOSITORY format: {github_repository}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Fetching traffic data for {repo_owner}/{repo_name}...")
    
    # Fetch traffic data
    traffic_data = get_traffic_data(repo_owner, repo_name, github_token)
    
    # Format and display summary
    summary = format_traffic_summary(repo_owner, repo_name, traffic_data)
    print(summary)
    
    # Save summary to file
    with open('traffic_summary.txt', 'w') as f:
        f.write(summary)
    
    # Save raw data as JSON
    with open('traffic_data.json', 'w') as f:
        json.dump(traffic_data, f, indent=2)
    
    print("\n✅ Traffic data saved to traffic_summary.txt and traffic_data.json")


if __name__ == '__main__':
    main()
