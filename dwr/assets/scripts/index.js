import './theme_switch';
//import './helper2';
import 'bootstrap';


import '../styles/styles.css';
import '../styles/styles.scss';


// import HTMX and inject it into the window scope
window.htmx = require('htmx.org');

window.addEventListener('load', () => {
    document.getElementById('message').textContent = 'REBUNDLED BY WEBPACK!';
}); 