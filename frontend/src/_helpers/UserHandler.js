import { ref } from 'vue';

const isLoggedIn = ref(false);
const currentUser = ref(null);

export default function UserHandler() {
  const url = 'http://localhost:5000/api';

  async function registerUser(form) {
    const { email, password } = form;
    const response = await fetch(`${url}/register`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
      }),
    });
    const result = await response.json();
    console.log(result);
  }

  async function performLogin(form) {
    const { email, password } = form;
    const response = await fetch(`${url}/login`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
      }),
    });
    const result = await response.json();

    if (result.error) {
      isLoggedIn.value = false;
      return;
    }

    isLoggedIn.value = true;
    currentUser.value = result;
    localStorage.setItem('user', JSON.stringify(result));
    console.log(result);
  }

  return {
    isLoggedIn,
    currentUser,
    performLogin,
    registerUser,
  };
}
