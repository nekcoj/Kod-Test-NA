<template>
  <Suspense>
    <template #default>
      <div class="p-d-flex p-flex-column">
      <div class="p-d-flex p-flex-column p-col 12 p-mx-auto">
        <div class="p-d-flex p-col-12 p-mx-auto">
          <label
            class="p-col-fixed p-text-left"
            :style="{width: '100px'}"
            for="email"
          >
            Email:
          </label>
          <InputText
            id="email"
            type="text"
            v-model="form.email"
            :class="{'p-invalid': !validateEmail() && form.email != ''}"
          />
        </div>
        <div class="p-d-flex p-col-12 p-mx-auto">
          <label
            class="p-col-fixed p-text-left"
            :style="{width: '100px'}"
            for="password"
          >
            Password:
          </label>
          <Password
            id="password"
            v-model="form.password"
            :class="{'p-invalid': !validatePassword() && form.password != ''}"
            :feedback="text === 'Register'"
          >
            <template #header>
              <h6>Pick a password</h6>
            </template>
            <template #footer>
              <Divider />
              <p class="p-mt-2">Requirements</p>
              <ul class="p-pl-2 p-ml-2 p-mt-0" style="line-height: 1.5">
                <li>At least one lowercase</li>
                <li>At least one uppercase</li>
                <li>At least one numeric</li>
                <li>Minimum 8 characters</li>
              </ul>
            </template>
          </Password>
        </div>
        <div class="p-d-flex p-col-12 p-jc-end">
          <Button :label="text" @click="performAction()"/>
        </div>
      </div>
        <div class="p-d-flex p-col-12 p-jc-center">
          <span v-if="text === 'Login'">
            No account? Register <router-link to="/register">here</router-link>.
          </span>
          <span v-else>
            Already have and account? Login <router-link to="/login">here</router-link>.
          </span>
        </div>
      </div>
    </template>
    <template #fallback>
      <h3>Laddar...</h3>
    </template>
  </Suspense>
</template>

<script>
import { reactive } from 'vue';
import UserHandler from '../_helpers/UserHandler';

export default {
  name: 'Form',
  props: {
    text: String,
  },
  setup(props) {
    const { performLogin, registerUser } = UserHandler();
    const form = reactive({
      email: '',
      password: '',
    });

    const validateEmail = () => {
      if (/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(form.email)) {
        return true;
      }
      return false;
    };

    const validatePassword = () => {
      if (/^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,})/.test(form.password)) {
        return true;
      }
      return false;
    };

    const performAction = async () => {
      if (!validateEmail() || !validatePassword()) return;
      let result;
      if (props.text === 'Register') {
        result = registerUser(form);
        console.log('Register', result);
        return;
      }

      result = performLogin(form);
      console.log(result);
    };

    return {
      form,
      performAction,
      validateEmail,
      validatePassword,
    };
  },
};
</script>

<style>

</style>
