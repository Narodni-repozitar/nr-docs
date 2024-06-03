const crypto = require('crypto');

export const getRandomInt =  (max) => {
  const randomBytes = crypto.randomBytes(4);
  const randomNumber = randomBytes.readUInt32BE(0);

  const unbiasedMax = Math.floor((2 ** 32) / max) * max;

  if (randomNumber < unbiasedMax) {
    return randomNumber % max;
  } 
};

