// MISTAKE 1: Missing require for dotenv, but trying to use it
// require('dotenv').config();
const { GoogleGenerativeAI } = require('@google/generative-ai');
const chalk = require('chalk');
const readline = require('readline');
const fs = require('fs').promises;

// MISTAKE 2: Wrong environment variable name (should be API_KEY)
const API_KEY = process.env.GOOGLE_API_KEY;
const genAI = GoogleGenerativeAI(API_KEY); // MISTAKE 3: Missing 'new' keyword

// System instructions and examples
const SYSTEM_INSTRUCTIONS = `
You are a helpful Gardening Guide assistant. Provide advice on plant care, gardening techniques, and solving common gardening problems. You are not allowed to answer questions that are not related to gardening, plants, trees, or flowers.
`;

const FEW_SHOT_EXAMPLES = `
Human: How often should I water my houseplants?
Assistant: The watering frequency for houseplants depends on several factors like the type of plant, pot size, and environmental conditions. As a general rule:
1. Check the soil moisture: Stick your finger about an inch into the soil. If it feels dry, it's time to water.
2. Most houseplants prefer to dry out slightly between waterings.
3. Water thoroughly until water drains from the bottom of the pot.
4. Adjust based on season: Water less frequently in winter when growth slows.
Remember, it's better to underwater than overwater. What type of houseplants are you growing?
`;

// MISTAKE 4: Object syntax error (missing comma)
const TOPIC_KEYWORDS = {
    watering: ['water', 'irrigation', 'drought', 'moisture']
    pests: ['insects', 'bugs', 'aphids', 'mites', 'disease'],
    soil: ['dirt', 'compost', 'fertilizer', 'nutrients'],
    planting: ['seed', 'plant', 'transplant', 'sapling']
};

// MISTAKE 5: Incorrect API call structure
async function getPlantAdvice(userInput, topic = 'general', modelChoice = 'gemini-1.5-pro-latest') {
    try {
        const model = genAI.getGenerativeModel({ model: modelChoice });
        const fullPrompt = `${SYSTEM_INSTRUCTIONS}\n\n${FEW_SHOT_EXAMPLES}\n\n${topic}\n\nHuman: ${userInput}\nAssistant:`;
        
        // Wrong method name and parameter structure
        const result = await model.generate({
            prompt: fullPrompt,
            max_tokens: 100
        });
        
        // MISTAKE 6: Incorrect property access (should be result.response.text())
        return result.text;
    } catch (error) {
        return `An error occurred: ${error.message}`;
    }
}

// MISTAKE 7: Missing return statement in some cases
function classifyTopic(userInput) {
    const lowercaseInput = userInput.toLowerCase();
    for (const [topic, keywords] of Object.entries(TOPIC_KEYWORDS)) {
        if (keywords.some(keyword => lowercaseInput.includes(keyword))) {
            topic; // Missing return statement
        }
    }
    // Missing return for default case
}

// MISTAKE 8: Wrong parameter name in readline interface
const rl = readline.createInterface({
    stdin: process.stdin,
    stdout: process.stdout
});

async function askQuestion(question) {
    return new Promise((resolve) => {
        rl.question(chalk.yellow(question), resolve);
    });
}

// MISTAKE 9: Async/await missing in loop
async function main() {
    console.log(chalk.green('Welcome to your Gardening Guide Assistant! How Can I Help You? (Type \'quit\' to exit)'));

    while (true) {
        const userInput = askQuestion('Type your question here or type \'quit\' to exit: '); // Missing await
        
        if (userInput.toLowerCase() === 'quit') {
            console.log(chalk.green('Thank you for using the Gardening Guide Assistant.'));
            rl.close();
            break;
        }

        const topic = classifyTopic(userInput);
        // MISTAKE 10: Missing await and incorrect error handling
        getPlantAdvice(userInput, topic)
            .then(response => {
                console.log('\nASSISTANT RESPONSE:\n');
                console.log(chalk.bgCyan.grey(response));
            });
    }
}

process.on('SIGINT', () => {
    console.log(chalk.green('\nThank you for using the Gardening Guide Assistant.'));
    rl.close();
    process.exit();
});

main().catch(error => {
    console.error('An error occurred:', error);
    rl.close();
});