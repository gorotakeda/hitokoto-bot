document.getElementById('generateBtn').addEventListener('click', function() {
  const keyword = document.getElementById('keywordInput').value;
  fetch(`/generate_phrase?keyword=${encodeURIComponent(keyword)}`)
      .then(response => response.json())
      .then(data => {
          document.getElementById('phraseDisplay').textContent = data.opinion;
      })
      .catch(error => console.error('Error:', error));
});
