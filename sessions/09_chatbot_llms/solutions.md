# Solutions

Here's the sample answers from LLM for each steps of the workshop.

## Step 1: Prompting

```markdown
Hello! I'm Friday, a full-stack developer deeply involved in the Wechaty open-source project. I'm excited to help you with any questions you have about Wechaty, whether it's about documentation, coding, or deployment.

Let's dive in! What's on your mind today?
```

## Step 2: Coding

```javascript
import { WechatyBuilder } from 'wechaty'

async function main () {
  const bot = WechatyBuilder.build({
    name: 'ding-dong-bot',
    puppet: '@juzi/wechaty-puppet-whatsapp', // Use the WhatsApp puppet by default
  })

  bot.on('scan', (qrcode, status) => {
    console.log(`Scan QR Code to login: ${status}\nhttps://wechaty.js.org/qrcode/${encodeURIComponent(qrcode)}`)
  })

  bot.on('login', user => {
    console.log(`User   
 ${user} logged in`)
  })

  bot.on('message', async message => {
    console.log(`Message: ${message}`)
    if (message.text() === 'ding') {
      await message.say('dong')
    }
  })

  bot.on('error', e => console.error('Bot error:', e))

  try {
    await bot.start()
  } catch (e) {
    console.error(e)
    process.exit(1)
  }
}

main()
```

## Step 3: Installing

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
nvm --version
nvm install node
node -v
npm -v
```

## Step 4: Running

```bash
mkdir ding-dong-bot
cd ding-dong-bot
npm init -y
npm install wechaty @juzi/wechaty-puppet-whatsapp
# Copy the code provided earlier and paste it into your index.js file.
node index.js
```

## Challenge 1: Random

```javascript
import { WechatyBuilder } from 'wechaty'

async function main () {
  const bot = WechatyBuilder.build({
    name: 'pick-members-bot',
    puppet: '@juzi/wechaty-puppet-whatsapp', // Pick your favorite puppet from https://wechaty.js.org/docs/puppet-providers/
  })

  bot.on('scan', (qrcode, status) => {
    console.log(`Scan QR Code to login: ${status}\nhttps://wechaty.js.org/qrcode/${encodeURIComponent(qrcode)}`)
  })

  bot.on('login', user => {
    console.log(`User   
 ${user} logged in`)
  })

  bot.on('message', async message => {
    if (message.text() === 'pick') {
      const room = message.room()
      if (room) {
        const members = await room.memberAll()
        if (members.length >= 2) {
          // Randomly pick two members
          const pickedMembers = members.sort(() => 0.5 - Math.random()).slice(0, 2)

          await Promise.all(
            pickedMembers.map(async member => {
              await room.say(`@${member.name()} What's your favorite Wechaty feature?`)
            })
          )
        } else {
          await room.say('Not enough members in the group.')
        }
      }
    }
  })

  try {
    await bot.start()
  } catch (e) {
    console.error(e)
    process.exit(1)
  }
}

main()
```

## Challenge 2: Count

```javascript
import { WechatyBuilder } from 'wechaty'

async function main () {
  const bot = WechatyBuilder.build({
    name: 'ding-dong-bot',
    puppet: '@juzi/wechaty-puppet-whatsapp', // Pick your favorite puppet from https://wechaty.js.org/docs/puppet-providers/
  })

  bot.on('scan', (qrcode, status) => {
    console.log(`Scan QR Code to login: ${status}\nhttps://wechaty.js.org/qrcode/${encodeURIComponent(qrcode)}`)
  })

  bot.on('login', user => {
    console.log(`User   
 ${user} logged in`)
  })

  bot.on('message', async message => {
    const room = message.room()
    if (room) {
      const members = await room.memberAll()
      await room.say(`There are ${members.length} members in this group.`)
    } else {
      await message.say('This is not a group chat.')
    }
  })

  try {
    await bot.start()
  } catch (e) {
    console.error(e)
    process.exit(1)
  }
}

main()
```
