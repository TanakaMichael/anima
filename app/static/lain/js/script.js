function addGif() {
    fetch('/lain/add', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        const img = document.createElement('img');
        img.src = data.image_url;
        img.className = 'gif-image';
        img.style.left = data.position.left + '%';
        img.style.top = data.position.top + '%';
        document.getElementById('image-container').appendChild(img);
    })
    .catch(error => console.error('Error:', error));
}
