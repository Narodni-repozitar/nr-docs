const crypto = require('crypto');

export const getRandomInt = async (max) => {
  const randomBytes = crypto.randomBytes(4);
  const randomValue = randomBytes.readUInt32BE(0);
  return randomValue % max;
};
