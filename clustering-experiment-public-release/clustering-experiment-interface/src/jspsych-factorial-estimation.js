import { Stopwatch, wait, filterInt } from './jspsych-utils'

var plugin = {};

plugin.info = {
  name: "factorial-estimation",
  parameters: {
    stimulus: {
      type: jsPsych.plugins.parameterType.HTML_STRING,
      default: undefined
    }
  }
};

plugin.trial = async function(displayElement, trial) {

  const settings = {
    stimulusDuration: 5000,
    countdownStartValue: 10,
    ...trial
  }

  displayElement.innerHTML = "";

  const factorialDisplay = document.createElement("p");
  factorialDisplay.innerText = "+";
  factorialDisplay.classList.add("factorial-display");
  displayElement.appendChild(factorialDisplay);

  // fixation time
  await wait(1000);
  // show stimulus
  factorialDisplay.innerText = settings.stimulus
  await wait(settings.stimulusDuration);

  factorialDisplay.innerHTML = `
    <p>You have <span id="factorial-countdown"></span> seconds to enter your best estimation.</p>
    <p>[enter] to continue.</p>
    <input id="factorial-input" pattern="[0-9]+"/>
  `

  const countdownSpan = factorialDisplay.querySelector('#factorial-countdown')
  const factorialInput = factorialDisplay.querySelector('#factorial-input')

  let inputCountdownValue = settings.countdownStartValue
  const stopwatch = new Stopwatch()

  const updateCountdownSpan = () => countdownSpan.innerText = inputCountdownValue.toString()


  factorialInput.focus()
  updateCountdownSpan()
  stopwatch.start()

  setInterval(() => {
    inputCountdownValue -= 1
    updateCountdownSpan()
  }, 1000)

  const keyUpListener = e => {
    if (e.key === 'Enter') {
      const userValue = filterInt(factorialInput.value)
      // if integer, end the trial
      if (!isNaN(userValue)) {
        const rt = stopwatch.stop()
        factorialInput.removeEventListener('keyup', keyUpListener)
        jsPsych.finishTrial({ ...settings, estimation: userValue, rt: rt })
      }
    }
  }

  factorialInput.addEventListener('keyup', keyUpListener)

};

export default function(jsPsych) {
  jsPsych.plugins["factorial-estimation"] = plugin;
}
