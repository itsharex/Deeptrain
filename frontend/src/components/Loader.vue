<template>
  <img src="/favicon.ico" alt="Deeptrain" />
  <div class="loader">
    <span class="bar" />
    <span class="bar" />
    <span class="bar" />
  </div>
</template>

<style scoped>
/**
  Copyright - 2023 aryamitra06 (Aryamitra Chaudhuri)
  License - MIT
 */

img {
  position: absolute;
  top: calc(50% - 52px);
  left: 50%;
  transform: translate(-50%, calc(-50% - 24px));
  width: 64px;
  height: 64px;
}

.loader {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
}

.bar {
  display: inline-block;
  width: 3px;
  height: 20px;
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 10px;
  animation: scale-up4 1s linear infinite;
}

.bar:nth-child(2) {
  height: 35px;
  margin: 0 5px;
  animation-delay: 0.25s;
}

.bar:nth-child(3) {
  animation-delay: 0.5s;
}

@keyframes scale-up4 {
  20% {
    background-color: #ffff;
    transform: scaleY(1.5);
  }

  40% {
    transform: scaleY(1);
  }
}
</style>
