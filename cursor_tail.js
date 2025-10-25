const ntrail = 7;
const dots = [];
const positions = [];
for (let i = 0; i < ntrail; i++) {
    const dot = document.createElement('div');
    dot.classList.add('cursortrail');
    document.body.appendChild(dot);
    dots.push(dot);
    positions.push({ x: window.innerWidth / 2, y: window.innerHeight / 2 });
}
document.addEventListener('mousemove', e => {
    positions.unshift({ x: e.pageX, y: e.pageY });
    positions.pop();
    dots.forEach((dot, i) => {
        const pos = positions[i];
        if (!pos) return;
        dot.style.left = pos.x + 'px';
        dot.style.top = pos.y + 'px';
        dot.style.opacity = `${1 - i / ntrail}`;
    });
});