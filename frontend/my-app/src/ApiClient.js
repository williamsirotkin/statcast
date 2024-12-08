class ApiClient {
    constructor(baseURL) {
      this.baseURL = baseURL;
    }
  
    async get(endpoint) {
        console.log(`${this.baseURL}${endpoint}`)
      try {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });
  
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
  
        return response.json();
      } catch (error) {
        throw new Error(`GET request failed: ${error.message}`);
      }
    }
  }

export default ApiClient