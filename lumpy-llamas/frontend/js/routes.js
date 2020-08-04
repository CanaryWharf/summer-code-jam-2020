import Home from './home-page.vue';
import calendarapp from './calendar-app.vue';

const routes = [
  {
    path: '/home',
    alias: '/',
    name: 'home_page',
    component: Home,
  },
  {
    path: '/calendarapp',
    alias: '/',
    name: 'calendarapp',
    component: calendarapp,
  },
];

export default routes;
