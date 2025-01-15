const FACTORIAL_INSTRUCTIONS = `
<h2>Instructions</h2>
<p>In this part of the study, you will estimate the result of multiplication expressions.</p>
<p>The problems are meant to be difficult - we do not expect you to make a correct response, just try your best.</p>
<p>A expression will appear after the fixation point. Once the screen says “enter your best estimation” , you have up to 10 seconds to complete your answer.</p>
<p>Once you are finished entering your answer, hit [enter] to continue to the next question.</p>
`;

function makeConfigurations(first, second, calibration, calibrationOrder) {
  const items = {
    ASC: "1x2x3x4x5x6x7x8",
    DESC: "8x7x6x5x4x3x2x1",
    "6": {
      ASC: { stimulus: "1x2x3x4x5x6", answer: 720 },
      DESC: { stimulus: "6x5x4x3x2x1", answer: 720 }
    },
    "10": {
      ASC: { stimulus: "1x2x3x4x5x6x7x8x9x10", answer: 3628800 },
      DESC: { stimulus: "10x9x8x7x6x5x4x3x2x1", answer: 3628800 }
    }
  };

  return [
    items[first],
    items[second],
    items[calibration][calibrationOrder],
    items[first],
    items[second]
  ];
}

const STIMULI_CONFIGURATIONS = {
  "0": makeConfigurations("ASC", "DESC", 6, "ASC"),
  "1": makeConfigurations("ASC", "DESC", 10, "ASC"),
  "2": makeConfigurations("DESC", "ASC", 6, "DESC"),
  "3": makeConfigurations("DESC", "ASC", 10, "DESC")
};

// uses state.participantNumber
export default function addFactorial(timeline, state) {
  let stimuli = null; // will be initiated

  // ## Instructions

  timeline.push({
    on_start: function() {
      stimuli = STIMULI_CONFIGURATIONS[state.participantNumber % 4];
    },
    type: "instructions",
    pages: [FACTORIAL_INSTRUCTIONS],
    show_clickable_nav: true,
    data: { questionId: "factorialInstructions" }
  });

  // ## Practice trial

  timeline.push({
    type: "html-keyboard-response",
    stimulus: "Hit [spacebar] to continue to try a practice trial.",
    choices: [32], // space
    data: { questionId: "continueToPracticeTrial" }
  });

  timeline.push({
    type: "factorial-estimation",
    stimulus: "4x5x7x9x3x1x2",
    data: { questionId: "practiceTrial" }
  });

  // ## Actual Trial Intro

  timeline.push({
    type: "html-keyboard-response",
    stimulus: `
      <p>We will continue to the experiment trials.</p>
      <p>Hit [spacebar] to start.</p>
    `,
    choices: [32], // space
    data: { questionId: "continueToExperimentalTrials" }
  });

  // ## Actual Trials - First Half

  for (let i = 0; i < 2; i++) {
    timeline.push({
      stimulus: () => stimuli[i],
      type: "factorial-estimation",
      data: { questionId: "factorialExperimental", factorialIndex: i }
    });
  }

  // ## Calibration

  timeline.push({
    type: "html-keyboard-response",
    choices: [32], // space,
    stimulus: () => {
      const problem = stimuli[2].stimulus;
      const answer = stimuli[2].answer;
      return `<p>Great job. Here is the correct answer to another multiplication problem:</p>
        <p class="factorial-display">${problem} = ${answer}</p>
        <p>Press [spacebar] to continue.`;
    },
    data: { questionId: "calibration" }
  });

  // Actual Trials - Second Half

  timeline.push({
    type: "html-keyboard-response",
    choices: [32], // space
    stimulus: `<p>In this next part of the study, you will estimate the result of more multiplication expressions.</p>

    <p>Once the screen says "enter your best estimation", you have up to 10 seconds to complete your answer.</p>

    <p>Once you are finished entering your answer, hit [enter] to continute to the next question.</p>

    <p>Hit [spacebar] to start.</p>
  `,
    data: { questionId: "postCalibrationInstructionReminder" }
  });

  for (let i = 0; i < 2; i++) {
    timeline.push({
      stimulus: () => stimuli[i + 3],
      type: "factorial-estimation",
      data: { questionId: "factorialExperimental", factorialIndex: i + 3 }
    });
  }

  timeline.push({
    type: "html-button-response",
    stimulus:
      "Thank you. Please answer a couple of questions regarding your estimation. Click continue to proceed.",
    choices: ["Continue"],
    data: { questionId: "continueToFactorialSurvey" }
  });

  timeline.push({
    type: "survey-text",
    questions: () => [
      {
        prompt: `<p>In your first trial, you estimated {${stimuli[0]}}.</p>
  <p>What was your strategy for estimating this multiplication expression?</p> `,
        required: true,
        placeholder: "",
        rows: 4,
        name: "firstTrialStrategy"
      }
    ],
    data: { questionId: "firstTrialStrategy" }
  });

  timeline.push({
    type: "survey-text",
    questions: () => [
      {
        prompt: `<p>In your second trial, you estimated {${stimuli[1]}}.</p>
  <p>What was your strategy for estimating this multiplication expression?</p> `,
        required: true,
        placeholder: "",
        rows: 4,
        name: "secondTrialStrategy"
      }
    ],
    data: { questionId: "secondTrialStrategy" }
  });

  timeline.push({
    type: "survey-text",
    questions: () => [
      {
        prompt: `
  <p>After you completed the first two trials, we provided the value of {${stimuli[2].stimulus}}. Then, we asked you to estimate {${stimuli[3]}} and {${stimuli[4]}} again.</p>

  <p>Did knowing the value of {${stimuli[2].stimulus}} help you estimate the third and fourth trial?</p>

  <p>Please describe how.</p>
          `,
        required: true,
        placeholder: "",
        rows: 4,
        name: "didCalibrationHelp"
      }
    ],
    data: { questionId: "didCalibrationHelp" }
  });

  timeline.push({
    type: "survey-html-form",
    html: () => `
        <p>If you had a calculator, would you get the same answer for {${stimuli[0]}} and {${stimuli[1]}}?</p>

        <input type="radio" required name="sameAnswer" id="Yes" value="Yes"> <label for="Yes">Yes</label><br>
        <input type="radio" required name="sameAnswer" id="No" value="No"> <label for="No">No</label>

        <p>Please describe why</p>
        <div><textarea cols="80" rows="5" name="calculatorDescription" required></textarea></div>
      `,
    data: { questionId: "calculatorSameAndWhy" }
  });
}
