function handler(event) {
    var request = event.request;
    var headers = request.headers;
    
    // Get the country code 
    var countryCode = headers['cloudfront-viewer-country'] ? headers['cloudfront-viewer-country'].value : 'US';
    
    // Default origin domain (US)
    var originDomain = 'dev.d11i4h2tcx4np2.amplifyapp.com'; // US
    
    // Map country codes to origins
    if (countryCode === 'IN') {
        originDomain = 'dev.d2y83y8kf9dqja.amplifyapp.com'; // India
    } else if (countryCode === 'US') {
        originDomain = 'dev.d11i4h2tcx4np2.amplifyapp.com'; // US
    } else {
        originDomain = 'dev.d2oj78aa375toh.amplifyapp.com'; // Rest of the world (Europe)
    }
    
    // Create a new request object with only the allowed fields
    var newRequest = {
        uri: request.uri,
        method: request.method,
        querystring: request.querystring,
        headers: request.headers
    };
    
    // Add the host header
    if (!newRequest.headers['host']) {
        newRequest.headers['host'] = { value: originDomain };
    } else {
        newRequest.headers['host'].value = originDomain;
    }
    
    return {
        statusCode: 302,
        statusDescription: 'Found',
        headers: {
            'location': { value: 'https://' + originDomain + request.uri }
        }
    };
}
