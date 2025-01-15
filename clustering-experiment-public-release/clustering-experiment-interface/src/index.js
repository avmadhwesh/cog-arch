/* global process */
// # CSS
// jsPsych
import "../jspsych-6.1.0/css/jspsych.css";
// Others
import "./clustering.css";
import "./addon-factorial-estimation.css";

// JS
// jsPsych
import "../jspsych-6.1.0/jspsych";
import "../jspsych-6.1.0/plugins/jspsych-instructions";
import "../jspsych-6.1.0/plugins/jspsych-survey-html-form";
import "../jspsych-6.1.0/plugins/jspsych-html-keyboard-response";
import "../jspsych-6.1.0/plugins/jspsych-html-button-response";
import "../jspsych-6.1.0/plugins/jspsych-survey-text";
import "../jspsych-6.1.0/plugins/jspsych-fullscreen";
// Others
import jsPsychFactorialEstimationPlugin from "./jspsych-factorial-estimation";
import jsPsychClusteringPlugin from "./jspsych-clustering";
import addFactorial from "./addon-factorial-estimation";
import { filterInt } from "./jspsych-utils";

import axios from "axios";

const CONSENT_FORM = `
<h2 id="consent-form-spatial-math-study-1">Consent Form | Spatial Math Study 1</h2>
<p>You are invited to participate in a research study of how people solve clustering problems. You were selected as a possible participant because you are an undergraduate student at the University of Minnesota and you are between 18-24 years of age. We ask that you read this form and ask any questions you may have before agreeing to be in the study.</p>
<p>This study is being conducted by Vijay Marupudi, Vimal Rao, Rina Harsch, and Jimin Park (graduate students, Educational Psychology Department); Dr. Jeffrey Bye (lecturer, Educational Psychology Department), and Dr. Sashank Varma (professor, Educational Psychology Department).</p>
<h2 id="background-information">Background Information</h2>
<p>The purpose of this study is to investigate how people solve clustering problems.</p>
<h2 id="procedures">Procedures</h2>
<p>If you agree to be in this study, we would ask you to complete two computerized tasks: (1) a clustering task and (2) an arithmetic estimation task.</p>
<p>In the clustering task, you will view a sequence of images, each containing fewer than 50 dots. You will use the mouse to draw circles around those dots that you judge to form clusters. In the arithmetic estimation task, you will view a sequence of arithmetic expression such as 6 x 6 x 6 x 6 x 6 x 6. You will be given 5 seconds to estimate the result of evaluating the expression.</p>
<p>Each task will begin with a few practice trials to familiarize you with how the stimuli will be presented and how you should respond. You will be allowed to take short breaks between tasks. The clustering task is relatively easy, and there is no “right” answer. The arithmetic estimation task is more difficult because of the large sizes of the problems and the limited time to answer each one, but again we are interested in your best estimate for each problem; no one will be able to compute an exact answer in 5 seconds.</p>
<p>The study will take approximately 50-60 minutes to complete.</p>
<h2 id="risks-and-benefits-of-being-in-the-study">Risks and Benefits of being in the Study</h2>
<p>The study has no known risks.</p>
<p>There are no expected benefits to participating in this study.</p>
<h2 id="compensation">Compensation:</h2>
<p>You will receive payment in the form of $15 for participating in this study. Your participation is entirely voluntary. You are free to withdraw at any time, and if you do, you will receive partial payment in the form of $5.</p>
<h2 id="confidentiality">Confidentiality</h2>
<p>The records of this study will be kept private. In any sort of report we might publish, we will not include any information that will make it possible to identify a subject. Research records will be stored securely and only researchers will have access to the records.</p>
<h2 id="voluntary-nature-of-the-study">Voluntary Nature of the Study</h2>
<p>Participation in this study is voluntary. Your decision whether or not to participate will not affect your current or future relations with the University of Minnesota. If you decide to participate, you are free to not answer any question or withdraw at any time without affecting those relationships.</p>
<h2 id="contacts-and-questions">Contacts and Questions</h2>
<p>For questions about the research study or results, or about other concerns, please contact the research team members:</p>
<p>Vijay Marupudi<br />
Ph.D. student<br />
612-636-6788<br />
<a href="mailto:marupudi@umn.edu" class="email">marupudi@umn.edu</a></p>
<p>Vimal Rao<br />
Ph.D. student<br />
612-625-5000<br />
<a href="mailto:rao00013@umn.edu" class="email">rao00013@umn.edu</a></p>
<p>Rina Harsch<br />
M.A. Student<br />
612-624-6083<br />
<a href="mailto:harsc008@umn.edu" class="email">harsc008@umn.edu</a></p>
<p>Jimin Park<br />
Ph.D. student<br />
612-636-6788<br />
<a href="mailto:park1481@umn.edu" class="email">park1481@umn.edu</a></p>
<p>Dr. Jeffrey Bye<br />
Lecturer<br />
612-624-6083<br />
<a href="mailto:jbye@umn.edu" class="email">jbye@umn.edu</a></p>
<p>Dr. Sashank Varma<br />
Professor<br />
612-625-6718<br />
<a href="mailto:sashank@umn.edu" class="email">sashank@umn.edu</a></p>
<p>This research has been reviewed and approved by an Institutional Review Board (IRB) within the Human Research Protections Program (HRPP). To share feedback privately with the HRPP about your research experience, call the Research Participants’ Advocate Line at 612-625-1650 or go to <a href="http://www.irb.umn.edu/report.html" class="uri">http://www.irb.umn.edu/report.html</a>. You are encouraged to contact the HRPP if:</p>
<ul>
<li>Your questions, concerns, or complaints are not being answered by</li>
<li>the research team.</li>
<li>You cannot reach the research team.</li>
<li>You want to talk to someone besides the research team.</li>
<li>You have questions about your rights as a research participant.</li>
<li>You want to get information or provide input about this research.</li>
</ul>
<p>You will be given a copy of this information to keep for your records at the end of the experiment, if you desire.</p>
<h2 id="statement-of-consent">Statement of Consent</h2>
<p>I have read the above information. I have asked questions and have received answers. I consent to participate in the study.</p>
<p>By signing this form, I also agree to give permission to the investigators to obtain my standardized test scores – all components of my ACT and/or SAT scores – maintained by the University of Minnesota</p>
<p>Name: <input name="name" required></p>
<p>Participant number: <input name="participantNumber" required></p>
<p>UMN Student ID: <input name="umnStudentId" required></p>
<p>Signature (type full name): <input name="signature" required></p>
<p>Date (mm/dd/yyyy): <input name="date" required></p>
`;

const INSTRUCTIONS = `
<h1 id="instructions">Instructions</h1>
<p>You will see some points displayed on the screen each trial. You task will be to draw circles around clusters of points. You can draw as many circles as you see fit. However, you will need to draw more than one circle per trial. The trial will end when you have drawn circles around all the dots.</p>
<p>You will draw the circles using your mouse. Click at the point you want to start drawing and trace the shape around the points you want to cluster. Release your mouse after you are done to complete the rest of the shape. You can drag beyond the rectangle where the points are displayed, so do not feel constrained by the borders.</p>
<p>You may take short breaks between trials, but otherwise <b>please give each task your undivided attention</b>.</p>
<p>Press [SPACEBAR] to continue to practice trials.</p>
`;

const DEMOGRAPHICS = `
<h1 id="demographics-form">Demographics Form</h1>
<ol type="1">
<li><p>Are you Hispanic or Latin(x)?</p>
<div>
<input type="radio" name="hispanic" id="hispanicYes" value="Yes"><label for="hispanicYes">Yes</label>
</div>
<div>
<input type="radio" name="hispanic" id="hispanicNo" value="No"><label for="hispanicNo">No</label>
</div></li>
<li><p>With which racial category or categories do you most closely identify:</p>
<div>
<input type="radio" name="racialCategories" id="racialCategoriesAmerican Indian / Alaskan Native" value="American Indian / Alaskan Native"><label for="racialCategoriesAmerican Indian / Alaskan Native">American Indian / Alaskan Native</label>
</div>
<div>
<input type="radio" name="racialCategories" id="racialCategoriesAsian" value="Asian"><label for="racialCategoriesAsian">Asian</label>
</div>
<div>
<input type="radio" name="racialCategories" id="racialCategoriesBlack or African American" value="Black or African American"><label for="racialCategoriesBlack or African American">Black or African American</label>
</div>
<div>
<input type="radio" name="racialCategories" id="racialCategoriesNative Hawaiian or Other Pacific Islander" value="Native Hawaiian or Other Pacific Islander"><label for="racialCategoriesNative Hawaiian or Other Pacific Islander">Native Hawaiian or Other Pacific Islander</label>
</div>
<div>
<input type="radio" name="racialCategories" id="racialCategoriesWhite" value="White"><label for="racialCategoriesWhite">White</label>
</div>
<div>
<input type="radio" name="racialCategories" id="racialCategoriesMultiracial" value="Multiracial"><label for="racialCategoriesMultiracial">Multiracial</label>
</div>
<p>If you picked “Multiracial”, please note which categories you identify with: <input type="text" name="racialCategoriesMultiracial"></p></li>
<li><p>With which gender identity do you most closely identify:</p>
<div>
<input type="radio" name="gender" id="genderMale" value="Male"><label for="genderMale">Male</label>
</div>
<div>
<input type="radio" name="gender" id="genderFemale" value="Female"><label for="genderFemale">Female</label>
</div>
<div>
<input type="radio" name="gender" id="genderNon-binary or gender non-confirming" value="Non-binary or gender non-confirming"><label for="genderNon-binary or gender non-confirming">Non-binary or gender non-confirming</label>
</div>
<div>
<input type="radio" name="gender" id="genderPrefer not to say" value="Prefer not to say"><label for="genderPrefer not to say">Prefer not to say</label>
</div>
<div>
<input type="radio" name="gender" id="genderPrefer to self describe" value="Prefer to self describe"><label for="genderPrefer to self describe">Prefer to self describe</label>
</div>
<p>If you picked “Prefer to self describe”, please describe here: <input type="text" name="genderSelfDescribe"></p></li>
<li><p>Are you left or right-handed?</p>
<div>
<input type="radio" name="handedness" id="handednessLeft-handed" value="Left-handed"><label for="handednessLeft-handed">Left-handed</label>
</div>
<div>
<input type="radio" name="handedness" id="handednessRight-handed" value="Right-handed"><label for="handednessRight-handed">Right-handed</label>
</div></li>
<li><p>What is your academic year?</p>
<div>
<input type="radio" name="academicYear" id="academicYearFreshman" value="Freshman"><label for="academicYearFreshman">Freshman</label>
</div>
<div>
<input type="radio" name="academicYear" id="academicYearSophomore" value="Sophomore"><label for="academicYearSophomore">Sophomore</label>
</div>
<div>
<input type="radio" name="academicYear" id="academicYearJunior" value="Junior"><label for="academicYearJunior">Junior</label>
</div>
<div>
<input type="radio" name="academicYear" id="academicYearSenior" value="Senior"><label for="academicYearSenior">Senior</label>
</div></li>
<li><p>What is your birthdate (mm/dd/yyyy)?</p>
<p><input type="text" name="birthdate"></p></li>
<li><p>What was the highest level of math that you took in high school?</p>
<div>
<input type="radio" name="mathLevel" id="mathLevelAlgebra" value="Algebra"><label for="mathLevelAlgebra">Algebra</label>
</div>
<div>
<input type="radio" name="mathLevel" id="mathLevelGeometry with an algebra prerequisite" value="Geometry with an algebra prerequisite"><label for="mathLevelGeometry with an algebra prerequisite">Geometry with an algebra prerequisite</label>
</div>
<div>
<input type="radio" name="mathLevel" id="mathLevelPre-calculus or trigonometry" value="Pre-calculus or trigonometry"><label for="mathLevelPre-calculus or trigonometry">Pre-calculus or trigonometry</label>
</div>
<div>
<input type="radio" name="mathLevel" id="mathLevelCalculus" value="Calculus"><label for="mathLevelCalculus">Calculus</label>
</div>
<div>
<input type="radio" name="mathLevel" id="mathLevelOther (please specify)" value="Other (please specify)"><label for="mathLevelOther (please specify)">Other (please specify)</label>
</div>
<p>If you picked “Other”, please note which your highest level: <input type="text" name="mathLevelOtherSpecification"></p></li>
<li><p>What is your <strong>college</strong> major / minor? (Indicate more than one if applicable.)</p>
<p><input type="text" name="majorMinor"></p></li>
<li><p>List your <strong>past semester</strong> colleges courses (designators and numbers) in mathematics?</p>
<textarea name="pastSemesterCourses" cols="80" rows="20"></textarea></li>
<li><p>List your <strong>current semester</strong> colleges courses (designators and numbers) in mathematics?</p>
<textarea name="currentSemesterCourses" cols="80" rows="20"></textarea></li>
</ol>
`;

const DEBRIEFING = `
<h1 id="debriefing-statement-spatial-math-study-1">Debriefing Statement | Spatial Math Study 1</h1>
<p>The purpose of this study is to investigate how young adults solve spatial math problems.</p>
<p>Previous studies have identified that there are some cognitive abilities that are available early in development and that form the basis for understanding mathematical concepts. For example, people have <strong>magnitude representations</strong> analogous to a mental number line, and use these representations to understand the size of numbers (Halberda, Mazzocco, &amp; Feigenson, 2008; Moyer &amp; Landauer, 1967; Sekuler &amp; Mierkiewicz, 1977). Most prior research has focused on number concepts. Comparatively little is known about the cognitive abilities that underlie understanding of spatial mathematical concepts.</p>
<p>The current study has the goal of finding evidence that the ability to efficiently <strong>cluster</strong> points in space is foundational for understanding concepts in graph theory, an abstract branch of mathematics. The experiment in which you participated is the first in this line of work. It investigates the nature of human clustering. (Subsequent experiments will attempt to connect the ability to cluster with the ability to solve graph theory problems.) You clustered a set of stimuli twice. Each stimulus was an arrangement of 10-40 points in a rectangle. For half, the points were “randomly” scattered. For the other half, the points were “non-randomly” scattered, i.e., contained naturally occurring clusters. The second time you clustered the stimuli, the points of half of the stimuli were flipped horizontally and vertically.</p>
<p>We will analyze your data to address four research questions:</p>
<ul>
<li>Is human clustering <strong>stable</strong>? Do people identify the same clusters when they view the same stimulus on multiple occasions?</li>
<li>If so, is this stability affected by the number of points? For example, are people less stable when there are more points?</li>
<li>Also, is this stability affected by randomness? Are people less stable when the points are scattered randomly?</li>
<li>Finally, is this stability affected by spatial transformation? Are people less stable when the points of a stimulus are flipped the second time they view it?</li>
</ul>
<p>This experiment is also investigating a question of individual differences. We will quantify your clustering performance, and see if it is associated with your ACT-Math score.</p>
<p>If you have any further questions, please ask the experimenter.</p>
<p>Vijay Marupudi<br />
Graduate Student, Educational Psychology<br />
<a href="mailto:marupudi@umn.edu" class="email">marupudi@umn.edu</a></p>
`;

const END_HTML = `
<p>Thank you for completing the study!</p>

<p>Save this link for a reference to the consent form: <a href="https://vijaymarupudi.gitlab.io/mncoglab/spatial-math-1-consent-form.html">https://vijaymarupudi.gitlab.io/mncoglab/spatial-math-1-consent-form.html</a></p>

<p><b>Please email the experimenter (mncoglab@gmail.com) with your participant number to receive payment!</b></p>
`;

 async function serverlog(message) {
   const participantNumber = state.participantNumber && state.participantNumber.toString() || "UNKNOWN";
   return axios.post("/api/clustering/log", { participantNumber, message })
 }


const state = {};

function getNavigatorData() {
  const _navigator = {};
  for (const i in navigator) {
    _navigator[i] = navigator[i];
  }
  return _navigator;
}

function normalText(text) {
  return "<div class='normal-text'>" + text + "</div>";
}

async function onExperimentEnd() {
  const experimentData = jsPsych.data.get().values();
  const interactionData = jsPsych.data.getInteractionData().values();
  const navigatorData = getNavigatorData();
  try {
    jsPsych.getDisplayElement().innerHTML = `<p>Uploading data, please wait...</p>`;
    await axios.post("/api/clustering/save", {
      participantNumber: state.participantNumber,
      data: {
        experimentData,
        interactionData,
        navigatorData
      }
    });
    jsPsych.getDisplayElement().innerHTML = normalText(END_HTML);
  } catch (err) {
    console.error(err);
    jsPsych.getDisplayElement().innerHTML = `<p><b>An error has occurred. Do not worry, you will still be paid. Please inform the experimenter of this error message.</b></p>

          <p>${err.name}: ${err.message}</p>`;
  }
}

async function main() {
  // Initiate custom jsPsych plugins
  jsPsychClusteringPlugin(jsPsych);
  jsPsychFactorialEstimationPlugin(jsPsych);

  const stimuliStore = {};

  const practiceUUIDs = jsPsych.randomization.shuffle(
    (await axios.get("stimuli/practice_uuids.json")).data
  );
  const setBlockUUIDConfiguration = (await axios.get(
    "stimuli/set_block_unique_uuids.json"
  )).data;
  const setBlockUUIDs = [];
  for (const set of Object.keys(setBlockUUIDConfiguration)) {
    for (const block of Object.keys(setBlockUUIDConfiguration[set])) {
      setBlockUUIDs.push(...setBlockUUIDConfiguration[set][block]);
    }
  }

  // Consolidate and remove duplicates
  const allUUIDs = [...practiceUUIDs, ...setBlockUUIDs].filter(
    (value, index, self) => {
      return self.indexOf(value) === index;
    }
  );

  const promises = allUUIDs.map(async uuid =>
    (await axios.get("stimuli/stimuli_json/" + uuid + ".json")).data
  );

  const allStimuli = await Promise.all(promises);
  allStimuli.forEach(stim => {
    stimuliStore[stim["unique_uuid"]] = stim;
  });

  const SET = 2;

  const timeline = [];

  const addBlockToTimeline = blockNumber => {
    const blockUUIDs = setBlockUUIDConfiguration[SET][blockNumber];
    const randomBlockUUIDs = jsPsych.randomization.shuffle(blockUUIDs);
    for (const stimulusUUID of randomBlockUUIDs) {
      timeline.push({
        type: "clustering",
        stimulus: stimuliStore[stimulusUUID],
        data: {
          block: blockNumber,
          set: SET
        }
      });
    }
  };

  const addBreak = () => {
    timeline.push({
      type: "html-keyboard-response",
      stimulus: `<p>Take a short break if you'd like.</p>
    <p>Press [spacebar] to continue</p>`,
      choices: [32],
      data: { questionId: "break" }
    });
  };

  const addIntroAndPracticeTrials = () => {
    // Mouse question
    timeline.push({
      type: "html-button-response",
      stimulus: `<p><b>We strongly recommend that you use a mouse for this study. If possible, please connect a mouse and use it.</b></p>
      <p>Are you going to use a mouse for this study?</p>`,
      choices: ["Yes", "No"],
      data: { questionId: "mouseQuestion" }
    });

    // Fullscreen
    timeline.push({
      type: "fullscreen",
      fullscreen_mode: true,
      data: { questionId: "fullscreenRequest" }
    });

    const subtimeline = []; // for looping during practice

    // Introduction
    subtimeline.push({
      type: "instructions",
      pages: [normalText(INSTRUCTIONS)],
      show_clickable_nav: true,
      data: { questionId: "clusteringInstructions" }
    });

    // Practice trials
    subtimeline.push(
      ...practiceUUIDs.map((uuid, idx) => ({
        type: "clustering",
        stimulus: stimuliStore[uuid],
        data: { questionId: "clusteringPracticeTrial", practiceTrialIdx: idx }
      }))
    );

    // Start over or Continue?
    subtimeline.push({
      type: "html-button-response",
      stimulus:
        "<p>Did you understand the task at hand? Click <i>continue</i> to start the experiment, or <i>start over</i> to practice again.</p>",
      choices: ["Start over", "Continue"],
      data: { questionId: "practiceStartOver" }
    });

    // Add to full timeline
    timeline.push({
      timeline: subtimeline,
      loop_function: function(data) {
        if (filterInt(data.last().values()[0].button_pressed) === 0) {
          return true;
        }
        return false;
      }
    });
  };

  const addNoticeHTML = (html, questionId) => {
    timeline.push({
      type: "html-button-response",
      stimulus: html,
      choices: ["Continue"],
      ...(questionId ? { data: { questionId: questionId } } : {})
    });
  };

  const addConsent = () => {
    // Consent
    timeline.push({
      timeline: [
        {
          type: "survey-html-form",
          html: normalText(CONSENT_FORM)
        }
      ],
      // Make sure participant number is an integer, and then sets it as a global
      // variable for factorial to use.
      loop_function: function() {
        const data = jsPsych.data
          .get()
          .last()
          .values()[0];
        const consentResponses = JSON.parse(data.responses);
        const participantNumber = filterInt(consentResponses.participantNumber);

        // if not a number, loop back
        if (isNaN(participantNumber)) {
          return true; // show consent form again
        } else {
          state.participantNumber = participantNumber;
        }

        axios.post(`/api/clustering/consent`, {
          participantNumber: state.participantNumber,
          data: jsPsych.data.get().values()
        });

        return false;
      },
      data: { questionId: "consentForm" }
    });
  };

  // Consent
  addConsent();
  // Intro and practice
  addIntroAndPracticeTrials();

  // 'Real trials begin here' notice
  addNoticeHTML(
    "<p>The experiment is about to begin.</p>",
    "experimentAboutToBegin"
  );
  addBlockToTimeline(1);
  addBreak();
  addBlockToTimeline(2);

  // Factorial
  addNoticeHTML(
    "<p>We will begin a different task. Take a short break if you'd like, and click continue to proceed to the next set.</p>",
    "switchToFactorial"
  );
  addFactorial(timeline, state);

  // Back to clustering
  addNoticeHTML(
    "<p>We are returning to the original task. Click continue to proceed.</p>",
    "returnToClustering"
  );
  addBlockToTimeline(3);
  addBreak();
  addBlockToTimeline(4);

  // Demographics

  addNoticeHTML(
    "<p>The trials have been completed. Please complete the following demographic form.</p>",
    "doneWithTrials"
  );

  timeline.push({
    type: "survey-html-form",
    html: normalText(DEMOGRAPHICS),
    data: { questionId: "demographics" }
  });

  // Debriefing statement
  timeline.push({
    type: "instructions",
    pages: [normalText(DEBRIEFING)],
    show_clickable_nav: true,
    data: { questionId: "debriefing" }
  });

  jsPsych.init({
    timeline: timeline,
    on_trial_finish: async data => {
      const trial_index = data.trial_index;
      serverlog(`Participant has completed trial_index: ${trial_index}`)
    },
    on_finish: onExperimentEnd
  });
}

// for debugging and development
window.tools = {
  endExperiment: onExperimentEnd
}

window.addEventListener("load", () => {
  document.body.innerHTML = `<h1>Loading...</h1>`;
  main();
});
