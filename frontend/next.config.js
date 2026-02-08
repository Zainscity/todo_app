/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    // Disable turbopack for now to avoid project root issues
    // turbopack: {
    //   root: __dirname,
    // },
  },
};

module.exports = nextConfig;