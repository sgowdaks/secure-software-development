const crypto = require('crypto');
var arguments = process.argv
const ENC_KEY = arguments[4];
const IV = arguments[5];

var encrypt = ((val) => {
  let cipher = crypto.createCipheriv('aes-256-cbc', ENC_KEY, IV);
  let encrypted = cipher.update(val, 'utf8', 'base64');
  encrypted += cipher.final('base64');
  return encrypted;
});

var decrypt = ((encrypted) => {
  let decipher = crypto.createDecipheriv('aes-256-cbc', ENC_KEY, IV);
  let decrypted = decipher.update(encrypted, 'base64', 'utf8');
  return (decrypted + decipher.final('utf8'));
});

if(arguments[2] == '-e'){
  var encrypted_key = encrypt(arguments[3]);
  console.log(encrypted_key);
}else{
  var original_phrase = decrypt(arguments[3]);
  console.log(original_phrase);
}
