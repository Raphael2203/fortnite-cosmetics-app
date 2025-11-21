interface ImportMetaEnv {
  readonly VITE_API_URL?: string;
  readonly BASE_URL?: string;
  readonly [key: string]: unknown;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
