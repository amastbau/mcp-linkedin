from linkedin_api import Linkedin
from fastmcp import FastMCP
import os
import json
import logging

mcp = FastMCP("mcp-linkedin")
logger = logging.getLogger(__name__)

_client = None

def get_client():
    global _client
    if _client is None:
        _client = Linkedin(
            os.getenv("LINKEDIN_EMAIL"),
            os.getenv("LINKEDIN_PASSWORD"),
            debug=True,
        )
    return _client


# ── Feed & Posts ─────────────────────────────────────────────────────────────

@mcp.tool()
def get_feed_posts(limit: int = 10, offset: int = 0) -> str:
    """Retrieve your LinkedIn feed posts."""
    client = get_client()
    try:
        post_urns = client.get_feed_posts(limit=limit, offset=offset)
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"Error: {e}"

    posts = ""
    for urn in post_urns:
        posts += f"Post by {urn['author_name']}: {urn['content']}\n\n"
    return posts or "No feed posts found."


@mcp.tool()
def get_post_comments(post_urn: str, comment_count: int = 100) -> str:
    """Get comments on a LinkedIn post.

    :param post_urn: The URN of the post
    :param comment_count: Maximum number of comments to retrieve
    """
    client = get_client()
    comments = client.get_post_comments(post_urn, comment_count=comment_count)
    return json.dumps(comments, indent=2, default=str)


@mcp.tool()
def get_post_reactions(post_urn: str, max_results: int = 50) -> str:
    """Get reactions (likes, etc.) on a LinkedIn post.

    :param post_urn: The URN of the post
    :param max_results: Maximum number of reactions to retrieve
    """
    client = get_client()
    reactions = client.get_post_reactions(post_urn, max_results=max_results)
    return json.dumps(reactions, indent=2, default=str)


# ── Profile ──────────────────────────────────────────────────────────────────

@mcp.tool()
def get_my_profile() -> str:
    """Get your own LinkedIn profile information."""
    client = get_client()
    profile = client.get_user_profile(use_cache=False)
    return json.dumps(profile, indent=2, default=str)


@mcp.tool()
def get_profile(public_id: str) -> str:
    """Get a LinkedIn user's profile by their public ID (the part in their profile URL).

    :param public_id: The public profile ID (e.g. 'john-doe-123')
    """
    client = get_client()
    profile = client.get_profile(public_id=public_id)
    return json.dumps(profile, indent=2, default=str)


@mcp.tool()
def get_profile_contact_info(public_id: str) -> str:
    """Get contact info (email, phone, etc.) for a LinkedIn profile.

    :param public_id: The public profile ID
    """
    client = get_client()
    info = client.get_profile_contact_info(public_id=public_id)
    return json.dumps(info, indent=2, default=str)


@mcp.tool()
def get_profile_experiences(urn_id: str) -> str:
    """Get work experiences for a LinkedIn profile.

    :param urn_id: The URN ID of the profile
    """
    client = get_client()
    experiences = client.get_profile_experiences(urn_id=urn_id)
    return json.dumps(experiences, indent=2, default=str)


@mcp.tool()
def get_profile_skills(public_id: str) -> str:
    """Get skills listed on a LinkedIn profile.

    :param public_id: The public profile ID
    """
    client = get_client()
    skills = client.get_profile_skills(public_id=public_id)
    return json.dumps(skills, indent=2, default=str)


@mcp.tool()
def get_profile_connections(urn_id: str) -> str:
    """Get connections for a LinkedIn profile.

    :param urn_id: The URN ID of the profile
    """
    client = get_client()
    connections = client.get_profile_connections(urn_id=urn_id)
    return json.dumps(connections, indent=2, default=str)


@mcp.tool()
def get_profile_network_info(public_id: str) -> str:
    """Get network info (follower count, connection count) for a profile.

    :param public_id: The public profile ID
    """
    client = get_client()
    info = client.get_profile_network_info(public_id)
    return json.dumps(info, indent=2, default=str)


@mcp.tool()
def get_profile_posts(public_id: str, post_count: int = 10) -> str:
    """Get recent posts by a LinkedIn user.

    :param public_id: The public profile ID
    :param post_count: Number of posts to retrieve
    """
    client = get_client()
    posts = client.get_profile_posts(public_id=public_id, post_count=post_count)
    return json.dumps(posts, indent=2, default=str)


# ── Notifications & Invitations ──────────────────────────────────────────────

@mcp.tool()
def get_invitations(start: int = 0, limit: int = 20) -> str:
    """Get pending connection invitations (incoming connection requests).

    :param start: Pagination start offset
    :param limit: Maximum number of invitations to retrieve
    """
    client = get_client()
    invitations = client.get_invitations(start=start, limit=limit)
    return json.dumps(invitations, indent=2, default=str)


@mcp.tool()
def get_profile_views() -> str:
    """Get the number of people who viewed your profile recently."""
    client = get_client()
    views = client.get_current_profile_views()
    return json.dumps(views, indent=2, default=str)


# ── Messaging ────────────────────────────────────────────────────────────────

@mcp.tool()
def get_conversations() -> str:
    """Get your LinkedIn message conversations (inbox)."""
    client = get_client()
    conversations = client.get_conversations()
    return json.dumps(conversations, indent=2, default=str)


@mcp.tool()
def get_conversation(conversation_urn_id: str) -> str:
    """Get messages in a specific conversation.

    :param conversation_urn_id: The URN ID of the conversation
    """
    client = get_client()
    conversation = client.get_conversation(conversation_urn_id=conversation_urn_id)
    return json.dumps(conversation, indent=2, default=str)


@mcp.tool()
def get_conversation_details(profile_urn_id: str) -> str:
    """Get conversation details with a specific person.

    :param profile_urn_id: The URN ID of the other person's profile
    """
    client = get_client()
    details = client.get_conversation_details(profile_urn_id=profile_urn_id)
    return json.dumps(details, indent=2, default=str)


# ── Search ───────────────────────────────────────────────────────────────────

@mcp.tool()
def search_people(
    keywords: str = "",
    current_company: str = "",
    keyword_title: str = "",
    keyword_first_name: str = "",
    keyword_last_name: str = "",
    network_depth: str = "",
    limit: int = 10,
) -> str:
    """Search for people on LinkedIn.

    :param keywords: General search keywords
    :param current_company: Filter by current company ID
    :param keyword_title: Filter by job title
    :param keyword_first_name: Filter by first name
    :param keyword_last_name: Filter by last name
    :param network_depth: Connection degree filter: 'F' (1st), 'S' (2nd), 'O' (3rd+)
    :param limit: Maximum number of results
    """
    client = get_client()
    kwargs = {}
    if keywords:
        kwargs["keywords"] = keywords
    if current_company:
        kwargs["current_company"] = [current_company]
    if keyword_title:
        kwargs["keyword_title"] = keyword_title
    if keyword_first_name:
        kwargs["keyword_first_name"] = keyword_first_name
    if keyword_last_name:
        kwargs["keyword_last_name"] = keyword_last_name
    if network_depth:
        kwargs["network_depth"] = network_depth
    results = client.search_people(limit=limit, **kwargs)
    return json.dumps(results, indent=2, default=str)


@mcp.tool()
def search_companies(keywords: str, limit: int = 10) -> str:
    """Search for companies on LinkedIn.

    :param keywords: Search keywords
    :param limit: Maximum number of results
    """
    client = get_client()
    results = client.search_companies(keywords=[keywords], limit=limit)
    return json.dumps(results, indent=2, default=str)


@mcp.tool()
def search_jobs(
    keywords: str,
    location: str = "",
    job_type: str = "",
    experience: str = "",
    remote: str = "",
    limit: int = 10,
) -> str:
    """Search for jobs on LinkedIn.

    :param keywords: Job search keywords
    :param location: Location filter
    :param job_type: Job type: F(ull-time), C(ontract), P(art-time), T(emporary), I(nternship), V(olunteer), O(ther)
    :param experience: Experience level: 1(Intern), 2(Entry), 3(Associate), 4(Mid-Senior), 5(Director), 6(Executive)
    :param remote: Remote filter: 1(On-site), 2(Remote), 3(Hybrid)
    :param limit: Maximum number of results
    """
    client = get_client()
    kwargs = {}
    if location:
        kwargs["location_name"] = location
    if job_type:
        kwargs["job_type"] = [job_type]
    if experience:
        kwargs["experience"] = [experience]
    if remote:
        kwargs["remote"] = [remote]

    jobs = client.search_jobs(keywords=keywords, limit=limit, **kwargs)

    job_results = ""
    for job in jobs:
        job_id = job["entityUrn"].split(":")[-1]
        try:
            job_data = client.get_job(job_id=job_id)
            title = job_data.get("title", "Unknown")
            company = job_data.get("companyDetails", {}).get(
                "com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany",
                {},
            ).get("companyResolutionResult", {}).get("name", "Unknown")
            loc = job_data.get("formattedLocation", "")
            desc = job_data.get("description", {}).get("text", "")
            job_results += f"**{title}** at {company} ({loc})\n{desc}\n\n"
        except Exception:
            job_results += f"Job ID {job_id} (details unavailable)\n\n"

    return job_results or "No jobs found."


# ── Companies ────────────────────────────────────────────────────────────────

@mcp.tool()
def get_company(public_id: str) -> str:
    """Get details about a company.

    :param public_id: The company's public ID (from its LinkedIn URL)
    """
    client = get_client()
    company = client.get_company(public_id)
    return json.dumps(company, indent=2, default=str)


@mcp.tool()
def get_company_updates(public_id: str, max_results: int = 10) -> str:
    """Get recent updates/posts from a company page.

    :param public_id: The company's public ID
    :param max_results: Maximum number of updates to retrieve
    """
    client = get_client()
    updates = client.get_company_updates(public_id=public_id, max_results=max_results)
    return json.dumps(updates, indent=2, default=str)


# ── Jobs ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def get_job(job_id: str) -> str:
    """Get detailed information about a specific job posting.

    :param job_id: The job ID
    """
    client = get_client()
    job = client.get_job(job_id=job_id)
    return json.dumps(job, indent=2, default=str)


@mcp.tool()
def get_job_skills(job_id: str) -> str:
    """Get skills required for a specific job posting.

    :param job_id: The job ID
    """
    client = get_client()
    skills = client.get_job_skills(job_id=job_id)
    return json.dumps(skills, indent=2, default=str)


# ── Schools ──────────────────────────────────────────────────────────────────

@mcp.tool()
def get_school(public_id: str) -> str:
    """Get details about a school/university.

    :param public_id: The school's public ID (from its LinkedIn URL)
    """
    client = get_client()
    school = client.get_school(public_id)
    return json.dumps(school, indent=2, default=str)


if __name__ == "__main__":
    mcp.run()
