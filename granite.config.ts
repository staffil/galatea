import { defineConfig } from '@apps-in-toss/web-framework/config';

export default defineConfig({
  appName: 'galatea-ai',
  brand: {
    displayName: '갈라테아 AI',
    primaryColor: '#3182F6',
    icon: "",
    bridgeColorMode: 'basic',
  },
  web: {
    host: '192.168.35.226', // PC의 실제 IP
    port: 8000,
    // ⛔ Granite는 Node 명령만 직접 실행할 수 있음.
    // ⭕ 따라서 Django 서버는 따로 수동으로 실행하고,
    // Granite dev에서는 "빈 명령"을 줘야 함.
    commands: {
    dev: "",
    build: "vite build",
    },
  },
  permissions: [],
  outdir: 'dist',
});
