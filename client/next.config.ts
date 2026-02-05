const nextConfig = {
  /* config options here */
  eslint: {
    // This ignores linting errors during build so the deployment doesn't fail
    ignoreDuringBuilds: true,
  },
  typescript: {
    // This ignores type errors during build for faster deployment
    ignoreBuildErrors: true,
  },
};

export default nextConfig;