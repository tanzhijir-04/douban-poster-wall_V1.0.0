(() => {
    const PLACEHOLDER_SVG = 'data:image/svg+xml,' + encodeURIComponent(
        '<svg xmlns="http://www.w3.org/2000/svg" width="150" height="225" viewBox="0 0 150 225">' +
        '<rect fill="#e5e5ea" width="150" height="225"/>' +
        '<text fill="#8e8e93" font-family="sans-serif" font-size="14" text-anchor="middle" x="75" y="118">缺失</text></svg>'
    );

    document.addEventListener('DOMContentLoaded', async () => {
        const wall = document.getElementById('posterWall');
        const loading = document.getElementById('loading');
        const countElem = document.getElementById('posterCount');

        try {
            const response = await fetch('poster_paths.json');
            if (!response.ok) throw new Error('未找到海报数据');

            const posterPaths = await response.json();
            countElem.textContent = posterPaths.length;
            loading.style.display = 'none';

            const fragment = document.createDocumentFragment();

            posterPaths.forEach(path => {
                const container = document.createElement('div');
                container.className = 'poster-item';

                const img = document.createElement('img');
                img.src = path;
                img.alt = '电影海报';
                img.loading = 'lazy';
                img.onerror = function () {
                    if (this._errored) return;
                    this._errored = true;
                    this.src = PLACEHOLDER_SVG;
                };

                container.appendChild(img);
                fragment.appendChild(container);
            });

            wall.appendChild(fragment);

        } catch (error) {
            loading.textContent = `加载失败：${error.message}`;
        }
    });
})();
