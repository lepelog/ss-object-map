module.exports = {
    root: true,
    parser: 'vue-eslint-parser',
    parserOptions: {
      parser: '@typescript-eslint/parser',
      project: 'tsconfig.json',
      ecmaVersion: 8,
      extraFileExtensions: ['.vue'],
    },
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
    ],
    globals: {
      Atomics: 'readonly',
      SharedArrayBuffer: 'readonly',
      nodecg: 'readonly',
      NodeCG: 'readonly',
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
    },
  };