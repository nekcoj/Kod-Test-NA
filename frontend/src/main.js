import { createApp } from 'vue';
import PrimeVue from 'primevue/config';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Divider from 'primevue/divider';
import Button from 'primevue/button';
import Card from 'primevue/card';
import App from './App.vue';
import router from './router';

import 'primeflex/primeflex.css';
import 'primeicons/primeicons.css';
import 'primevue/resources/primevue.min.css';
import 'primevue/resources/themes/bootstrap4-light-blue/theme.css';

createApp(App)
  .use(router)
  .use(PrimeVue)
  .component('InputText', InputText)
  .component('Password', Password)
  .component('Divider', Divider)
  .component('Button', Button)
  .component('Card', Card)
  .mount('#app');
