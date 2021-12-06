FROM node:16-alpine AS base
ARG PNPM_VERSION=6.22.2
RUN npm --global install pnpm@${PNPM_VERSION}
WORKDIR /app
# ----------

FROM base AS builder
ARG BACKEND_PREFIX_URL
COPY package.json ./
COPY pnpm-lock.yaml ./
RUN --mount=type=cache,id=pnpm-store,target=/root/.pnpm-store \
  pnpm install --frozen-lockfile

COPY *.config.cjs svelte.config.js ./
COPY static ./static
COPY src ./src
RUN pnpm run build
# ----------------

FROM base AS production
COPY package.json ./
COPY pnpm-lock.yaml ./
RUN --mount=type=cache,id=pnpm-store,target=/root/.pnpm-store\
  pnpm install --frozen-lockfile --prod
COPY --from=builder /app/build ./build
EXPOSE 3000
ENTRYPOINT ["node", "build/index.js"]
