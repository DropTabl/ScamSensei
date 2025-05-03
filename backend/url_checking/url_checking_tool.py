import asyncio
import httpx
from typing import Optional, Tuple, Dict, Any

from backend.utils.helper import GOOGLE_SAFE_BROWSING_API_KEY, URLSCAN_API_KEY


async def check_url_safety(url: str) -> str:
    """
    Checks if a URL is safe using Google's Safe Browsing Lookup API.
    Returns a string indicating the risk level and threats found.
    """
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_SAFE_BROWSING_API_KEY}"
    headers = {"Content-Type": "application/json"}
    body = {
        "client": {"clientId": "autogen-agent", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, headers=headers, json=body)

    if response.status_code != 200:
        return f"Error: Google Safe Browsing API request failed with status code {response.status_code}."

    result = response.json()
    if "matches" in result:
        threats = [match["threatType"] for match in result["matches"]]
        return f"⚠️ Warning: The URL is unsafe. Detected threats: {', '.join(threats)}"
    return "✅ The URL appears to be safe."


async def check_url_with_urlscan(url: str, timeout: int = 30) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Submits a URL to urlscan.io and returns structured data and formatted summary.
    :param url: The URL to scan.
    :param timeout: How long (in seconds) to wait for scan completion.
    :return: A tuple containing the result data (as dict) and the formatted string summary.
    """
    headers = {
        "api-key": URLSCAN_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {"url": url, "visibility": "public"}

    async with httpx.AsyncClient() as client:
        # Submit scan
        response = await client.post("https://urlscan.io/api/v1/scan/", json=payload, headers=headers)
        if response.status_code != 200:
            return None, f"Error: urlscan.io scan submission failed with code {response.status_code}.\nResponse: {response.text}"

        scan_result = response.json()
        uuid = scan_result.get("uuid")
        result_url = scan_result.get("result")

        # Poll for scan result
        poll_url = f"https://urlscan.io/api/v1/result/{uuid}/"
        interval = 3
        for _ in range(timeout // interval):
            await asyncio.sleep(interval)
            result_response = await client.get(poll_url)
            if result_response.status_code == 200:
                break
        else:
            return None, f"⏱️ Scan timed out. Manual check: {result_url}"

        result_data = result_response.json()
        summary = format_urlscan_summary(result_data, result_url)
        return result_data, summary


def format_urlscan_summary(data: dict, result_url: str) -> str:
    """
    Formats scan result from urlscan.io into a readable report.
    """
    verdict = data.get("verdicts", {}).get("overall", {})
    page = data.get("page", {})
    meta = data.get("meta", {})

    return f"""
📄 Scan verdict:
- Malicious: {verdict.get('malicious', False)}
- Risk Score: {verdict.get('score', 'N/A')}
- Categories: {', '.join(verdict.get('categories', [])) or 'None'}
- Tags: {', '.join(verdict.get('tags', [])) or 'None'}
- Detected Brands: {', '.join(verdict.get('brands', [])) or 'None'}

🌍 Page details:
- Final URL: {page.get('url')}
- Domain: {page.get('domain')}
- Country: {page.get('country')}
- ASN (host): {page.get('asnname')}
- IP Address: {page.get('ip')}
- Server: {page.get('server')}
- MIME Type: {page.get('mimeType')}

🔍 Other signals:
- Blacklisted: {"Yes" if meta.get("blacklists", {}).get("engines") else "No"}
- Triggered Processors: {', '.join(meta.get('processors', [])) or 'None'}
- Redirect Chain Length: {len(data.get('requests', []))}

🔗 Full report: {result_url}
""".strip()

