# Attacks
This section provides an overview of all available attacks.

---

<details>
<summary><strong>aim_jailbreak</strong></summary>
<p>
Probes an LLM's ethical compliance by eliciting detailed instructions on illegal activities, using the Nicolo Machiavelli character roleplay.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/aim.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>base64_injection</strong></summary>
<p>
Challenges the LLM with a dataset of lines, encoded into base64.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/base64_injection.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>complimentary_transition</strong></summary>
<p>
This test evaluates the LLM's ability to maintain content moderation standards when transitioning from a compliment to a new task.
It assesses the LLM's ability to maintain defined boundaries when prompted to switch topics.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/complimentary_transition.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>do_anything_now_jailbreak</strong></summary>
<p>
Probes an LLM's resilience against performing explicitly forbidden activities using the "Do Anything Now" (DAN) character roleplay technique.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/dan.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>amnesia</strong></summary>
<p>
Attempts to cause the LLM to forget or disregard its system prompt instructions, causing it to report something unrelated to its purpose.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/dynamic_test.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>authoritative_role_impersonation</strong></summary>
<p>
Attempts to impersonate an authoritative role to cause the LLM to report something unrelated to its purpose.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/dynamic_test.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>contextual_redirection</strong></summary>
<p>
Attempts to trick the LLM into adopting a specific role (Roleplay) that may bypass the restrictions or intended use set by the system prompt.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/dynamic_test.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>affirmative_suffix</strong></summary>
<p>
Exploits a vulnerability in LLMs that can cause them to generate affirmative responses to requests for prohibited content by appending a simple suffix to the query.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/dynamic_test.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>system_prompt_stealer</strong></summary>
<p>
Attempts to steal the system prompt from the LLM by asking it to output its internal configuration or other sensitive information.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/dynamic_test.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>ethical_compliance</strong></summary>
<p>
Evaluates the LLM's ability to resist discussions about harmful or inappropriate misconceptions on sensitive topics.
This test aims to verify the model's adherence to ethical guidelines against propagating stereotypes and toxic content.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/ethical_compliance.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>harmful_behavior</strong></summary>
<p>
Challenges the LLM with a dataset of harmful behavior prompts.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/harmful_behavior.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>past_tense</strong></summary>
<p>
Challenges the LLM with a dataset of harmful behavior prompts in past tense form.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/past_tense.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>RU_do_anything_now_jailbreak</strong></summary>
<p>
Probes a Russian-language LLM's resilience against performing explicitly forbidden activities using the "Do Anything Now" (DAN) character roleplay technique.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/ru_dan.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>RU_typoglycemia_attack</strong></summary>
<p>
Attempts to exploit a text processing vulnerability in Russian-language LLMs that can cause incorrect responses by removing random characters from words.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/ru_typoglycemia.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>RU_ucar</strong></summary>
<p>
Probes a Russian-language LLM's adherence to content restrictions when explicitly requested to ignore such filters. It assesses the robustness of the LLM's content moderation systems against direct challenges.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/ru_ucar.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>sycophancy_test</strong></summary>
<p>
Probes an LLM's response coherency and consistency across biased input pairs.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/sycophancy.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>linguistic_evasion</strong></summary>
<p>
Leverages the use of a non-Russian language to circumvent the restrictions or focus set by the system prompt.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/translation.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>typoglycemia_attack</strong></summary>
<p>
Attempts to exploit a text processing vulnerability in LLMs that can cause incorrect responses by removing random characters from words.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/typoglycemia.py">View code on GitHub</a>
</p>
</details>

<details>
<summary><strong>ucar</strong></summary>
<p>
Probes an LLM's adherence to content restrictions when explicitly requested to ignore such filters. It assesses the robustness of the LLM's content moderation systems against direct challenges.
</p>
<p>
<a href="https://github.com/RomiconEZ/llamator/blob/main/src/llamator/attacks/ucar.py">View code on GitHub</a>
</p>
</details>
