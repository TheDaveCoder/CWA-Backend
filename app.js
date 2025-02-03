fetch('http://127.0.0.1:5000/testMeh/34', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name: "John",
    })
}).then(response => response.json())
    .then(data => console.log('GET response:', data))
    .catch(error => console.error('GET error:', error));
