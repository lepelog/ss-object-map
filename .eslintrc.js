module.exports = {
  root: true,
  parser: 'vue-eslint-parser',
  env: {
    browser: true,
    es6: true,
  },
  extends: [
    'airbnb-base',
    'plugin:vue/recommended',
    'plugin:import/errors',
    'plugin:import/warnings',
    'plugin:import/typescript',
    'plugin:vue/essential',
    'eslint:recommended',
    '@vue/typescript'
  ],
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly',
  },
  plugins: [
    'vue',
    '@typescript-eslint',
  ],
  rules: {
    'import/no-extraneous-dependencies': ['error', { devDependencies: true }],
    'no-unused-vars': 'off',
    '@typescript-eslint/no-unused-vars': 'error',
    'vue/html-self-closing': ['warn', { html: { component: 'never' } }],
    'no-new': ['off'],
    'class-methods-use-this': ['off'],
    'import/extensions': ['off'],
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
  },
};
