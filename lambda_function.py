"""
Lambda@Edge function for geolocation routing between regional Amplify apps.
This function routes users to different regional origins based on their country.
"""
import json

def lambda_handler(event, context):
    """
    Route users to different origins based on their geographic location.
    
    Args:
        event: The CloudFront event
        context: Lambda context object
    
    Returns:
        Modified request with appropriate origin
    """
    # Get the request and headers from the CloudFront event
    request = event['Records'][0]['cf']['request']
    headers = request['headers']
    
    # Log the initial request details
    print(f"Original request: {json.dumps(request, default=str)}")
    
    # Extract viewer's country from CloudFront headers
    country = 'UNKNOWN'
    if 'cloudfront-viewer-country' in headers:
        country = headers['cloudfront-viewer-country'][0]['value']
    
    print(f'Viewer country: {country}')
    
    # Set the appropriate origin based on country
    if country == 'US':
        # US origin
        origin_domain = 'dev.d11i4h2tcx4np2.amplifyapp.com'
        print(f'Routing to US origin: {origin_domain}')
    elif country == 'IN':
        # India origin
        origin_domain = 'dev.d2y83y8kf9dqja.amplifyapp.com'
        print(f'Routing to India origin: {origin_domain}')
    else:
        # Default (Europe) origin
        origin_domain = 'dev.d2oj78aa375toh.amplifyapp.com'
        print(f'Routing to default (Europe) origin: {origin_domain}')
    
    # Set the origin in the request object
    request['origin'] = {
        'id': origin_domain,  # Origin ID must match what's in CloudFront
        'custom': {
            'domainName': origin_domain,
            'port': 443,
            'protocol': 'https',
            'path': '',
            'sslProtocols': ['TLSv1', 'TLSv1.1', 'TLSv1.2'],
            'readTimeout': 5,
            'keepaliveTimeout': 5,
            'customHeaders': {}
        }
    }
    
    # CRITICAL FIX: Update the Host header to match the origin domain
    # This ensures the request is accepted by the origin server
    headers['host'] = [{
        'key': 'Host',
        'value': origin_domain
    }]
    
    # Log the final modified request
    print(f"Modified request: {json.dumps(request, default=str)}")
    
    # Return the modified request to CloudFront
    return request
