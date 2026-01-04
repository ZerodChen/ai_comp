import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useAppStore = defineStore('app', () => {
  const isIdeMode = ref(true); // Default to IDE mode

  function toggleMode() {
    isIdeMode.value = !isIdeMode.value;
  }

  return { isIdeMode, toggleMode };
});
