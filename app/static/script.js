
function performRoundup() {
    fetch('/roundup', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('result').innerText = `Saved £${(data.saved_minor / 100).toFixed(2)} to savings goal.`;
                document.getElementById('result').classList.add('success');
            } else {
                document.getElementById('result').innerText = `Error: ${data.error}`;
            }
        })
        .catch(err => {
            document.getElementById('result').innerText = `Error: ${err}`;
        });
}