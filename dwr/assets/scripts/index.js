import './helper1';
import './helper2';

window.addEventListener('load', () => {
    document.getElementById('message').textContent = 'REBUNDLED BY WEBPACK!';
}); 