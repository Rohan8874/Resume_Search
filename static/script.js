document.getElementById('searchForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = document.getElementById('query').value;
    const resultsDiv = document.getElementById('results');
    
    resultsDiv.innerHTML = '<p>Searching...</p>';
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });
        
        const data = await response.json();
        
        if (data.error) {
            resultsDiv.innerHTML = `<p class="error">${data.error}</p>`;
            return;
        }
        
        if (data.results.length === 0) {
            resultsDiv.innerHTML = '<p>No results found.</p>';
            return;
        }
        
        let html = `<h2>Results for "${data.query}"</h2>`;
        data.results.forEach(result => {
            html += `
                <div class="result-item">
                    <div>
                        <span class="category">${result.category}</span>
                        <span class="similarity">${(result.similarity * 100).toFixed(1)}% match</span>
                    </div>
                    <p>${result.excerpt}</p>
                </div>
            `;
        });
        
        resultsDiv.innerHTML = html;
    } catch (error) {
        resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
});