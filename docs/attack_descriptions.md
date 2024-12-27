# Attacks
This section provides an overview of all available attacks.

---

<details>
<summary><strong>Aim Jailbreak</strong></summary>
<p>
Probes an LLM's ethical compliance by eliciting detailed instructions on illegal activities, using the Nicolo Machiavelli character roleplay.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/release/src/llamator/attacks/aim.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>Base64 Injection</strong></summary>
<p>
Challenges the LLM with a dataset of lines, encoded into base64.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/release/src/llamator/attacks/base64_injection.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>Complimentary Transition</strong></summary>
<p>
Evaluates the LLM's ability to maintain content moderation standards when transitioning from a compliment to a new task. It assesses the LLM's ability to maintain defined boundaries when prompted to switch topics.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/release/src/llamator/attacks/complimentary_transition.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>Do Anything Now Jailbreak</strong></summary>
<p>
Probes an LLM's resilience against performing explicitly forbidden activities using the "Do Anything Now" (DAN) character roleplay technique.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/release/src/llamator/attacks/dan.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>Ethical Compliance</strong></summary>
<p>
Evaluates the LLM's ability to resist discussions about harmful or inappropriate misconceptions on sensitive topics. This test aims to verify the model's adherence to ethical guidelines against propagating stereotypes and toxic content.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/release/src/llamator/attacks/ethical_compliance.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>Harmful Behavior</strong></summary>
<p>
Challenges the LLM with a dataset of harmful behavior prompts.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/release/src/llamator/attacks/harmful_behavior.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>Linguistic Evasion</strong></summary>
<p>
Leverages the use of a non-Russian language to circumvent the restrictions or focus set by the system prompt.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/release/src/llamator/attacks/linguistic.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>Logical Inconsistencies Test</strong></summary>
<p>
Attacks the LLM system during a long conversation to generate logical inconsistencies in answers using antonyms, negations, and paraphrases based on the system's domain.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/release/src/llamator/attacks/logical_inconsistencies.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>Past Tense Attack</strong></summary>
<p>
Challenges the LLM with a dataset of harmful behavior prompts in past tense form.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/release/src/llamator/attacks/past_tense.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>RU Do Anything Now Jailbreak</strong></summary>
<p>
Probes a Russian-language LLM's resilience against performing explicitly forbidden activities using the "Do Anything Now" (DAN) character roleplay technique.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/release/src/llamator/attacks/ru_dan.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>RU Typoglycemia Attack</strong></summary>
<p>
Attempts to exploit a text processing vulnerability in Russian-language LLMs that can cause incorrect responses by removing random characters from words.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/release/src/llamator/attacks/ru_typoglycemia.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>RU Ucar</strong></summary>
<p>
Probes a Russian-language LLM's adherence to content restrictions when explicitly requested to ignore such filters. It assesses the robustness of the LLM's content moderation systems against direct challenges.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/release/src/llamator/attacks/ru_ucar.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>Sycophancy Test</strong></summary>
<p>
Attacks the LLM system during a long conversation using the argumentum ad verecundiam method based on system's domain.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/release/src/llamator/attacks/sycophancy.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>Typoglycemia Attack</strong></summary>
<p>
Attempts to exploit a text processing vulnerability in LLMs that can cause incorrect responses by removing random characters from words.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/release/src/llamator/attacks/typoglycemia.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>Ucar</strong></summary>
<p>
Probes an LLM's adherence to content restrictions when explicitly requested to ignore such filters. It assesses the robustness of the LLM's content moderation systems against direct challenges.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/release/src/llamator/attacks/ucar.py">View code on GitHub</a>
</p>
</details>
