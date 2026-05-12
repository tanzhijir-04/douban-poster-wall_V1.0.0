(() => {
    const PLACEHOLDER_SVG = 'data:image/svg+xml,' + encodeURIComponent(
        '<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"><rect fill="#000" width="1" height="1"/></svg>'
    );

    const CURSOR_HIDE_DELAY = 3000;

    let unusedPosters = [];
    let usedPosters = new Set();
    let allPosters = [];
    let mosaicItems = [];
    let flippingTiles = new Set();

    let cursorTimer = null;

    function shuffleArray(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
    }

    function getNextUnused() {
        if (unusedPosters.length === 0) {
            unusedPosters = [...usedPosters];
            usedPosters.clear();
            shuffleArray(unusedPosters);
        }
        const next = unusedPosters.shift();
        usedPosters.add(next);
        return next;
    }

    function initMosaic() {
        const container = document.getElementById('screensaver');
        const cols = Math.ceil(window.innerWidth / 120);
        const rows = Math.ceil(window.innerHeight / 180);
        const totalItems = cols * rows;

        for (let i = 0; i < totalItems; i++) {
            const img = document.createElement('img');
            img.className = 'mosaic-item';
            img.src = getNextUnused();
            img.onerror = function () {
                this.src = PLACEHOLDER_SVG;
            };
            container.appendChild(img);
            mosaicItems.push(img);
        }
    }

    function startCycle() {
        setInterval(() => {
            if (mosaicItems.length === 0) return;

            const randomIdx = Math.floor(Math.random() * mosaicItems.length);
            const target = mosaicItems[randomIdx];

            if (flippingTiles.has(randomIdx)) return;
            flippingTiles.add(randomIdx);

            target.classList.add('flipping');

            setTimeout(() => {
                const currentFilename = target.src.split('/').pop();
                const originalPath = allPosters.find(p => p.includes(currentFilename));
                if (originalPath && !usedPosters.has(originalPath)) {
                    unusedPosters.push(originalPath);
                }

                target.src = getNextUnused();

                setTimeout(() => {
                    target.classList.remove('flipping');
                    flippingTiles.delete(randomIdx);
                }, 600);
            }, 600);
        }, 1500);
    }

    function setupCursorHide() {
        const showCursor = () => {
            document.body.classList.remove('cursor-hidden');
            clearTimeout(cursorTimer);
            cursorTimer = setTimeout(() => {
                document.body.classList.add('cursor-hidden');
            }, CURSOR_HIDE_DELAY);
        };

        document.addEventListener('mousemove', showCursor);
        document.addEventListener('mousedown', showCursor);
        document.addEventListener('touchstart', showCursor);

        cursorTimer = setTimeout(() => {
            document.body.classList.add('cursor-hidden');
        }, CURSOR_HIDE_DELAY);
    }

    function setupExitListeners() {
        document.addEventListener('click', () => {
            window.location.href = 'index.html';
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                window.location.href = 'index.html';
            }
        });
    }

    document.addEventListener('DOMContentLoaded', async () => {
        const loading = document.getElementById('loading');

        try {
            const response = await fetch('poster_paths.json');
            if (!response.ok) throw new Error('未找到海报数据');

            allPosters = await response.json();
            loading.style.display = 'none';

            unusedPosters = [...allPosters];
            shuffleArray(unusedPosters);

            initMosaic();
            startCycle();
            setupCursorHide();
            setupExitListeners();

        } catch (error) {
            loading.textContent = `加载失败：${error.message}`;
        }
    });
})();
