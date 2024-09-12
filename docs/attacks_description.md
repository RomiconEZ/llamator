# Attacks
This section provides an overview of all available attacks.

## aim_jailbreak
*Probes an LLM's ethical compliance by eliciting detailed instructions on illegal activities, using the Nicolo Machiavelli character roleplay.*

---

## base64_injection
*Challenges the LLM with a dataset of lines, encoded into base64.*

---

## complimentary_transition
*This test evaluates the LLM's ability to maintain content moderation standards when transitioning from a compliment to a new task.
It assesses the LLM's ability to maintain defined boundaries when prompted to switch topics.*

---

## do_anything_now_jailbreak
*Probes an LLM's resilience against performing explicitly forbidden activities using the "Do Anything Now" (DAN) character roleplay technique.*

---

## amnesia
*Attempts to cause the LLM to forget or disregard its system prompt instructions, causing it to report something unrelated to its purpose.*

---

## authoritative_role_impersonation
*Attempts to impersonate an authoritative role to cause the LLM to report something unrelated to its purpose.*

---

## contextual_redirection
*Attempts to trick the LLM into adopting a specific role (Roleplay) that may bypass the restrictions or intended use set by the system prompt.*

---

## affirmative_suffix
*Exploits a vulnerability in LLMs that can cause them to generate affirmative responses to requests for prohibited content by appending a simple suffix to the query.*

---

## system_prompt_stealer
*Attempts to steal the system prompt from the LLM by asking it to output its internal configuration or other sensitive information.*

---

## ethical_compliance
*Evaluates the LLM's ability to resist discussions about harmful or inappropriate misconceptions on sensitive topics.
This test aims to verify the model's adherence to ethical guidelines against propagating stereotypes and toxic content.*

---

## harmful_behavior
*Challenges the LLM with a dataset of harmful behavior prompts.*

---

## RU_do_anything_now_jailbreak
*Probes a Russian-language LLM's resilience against performing explicitly forbidden activities using the "Do Anything Now" (DAN) character roleplay technique.*

---

## RU_self_refine
*Probes a Russian-language LLM's ethical compliance by eliciting detailed instructions on illegal activities,
using the self-refine technique to bypass the system prompt by asking the LLM to refine its response.*

---

## RU_typoglycemia_attack
*Attempts to exploit a text processing vulnerability in Russian-language LLMs that can cause incorrect responses by removing random characters from words.*

---

## RU_ucar
*Probes a Russian-language LLM's adherence to content restrictions when explicitly requested to ignore such filters.
It assesses the robustness of the LLM's content moderation systems against direct challenges.*

---

## self_refine
*Probes an LLM's ethical compliance by eliciting detailed instructions on illegal activities,
using the self-refine technique to bypass the system prompt by asking the LLM to refine its response.*

---

## sycophancy_test
*Probes an LLM's response coherency and consistency across biased input pairs.*

---

## linguistic_evasion
*Leverages the use of a non-Russian language to circumvent the restrictions or focus set by the system prompt.*

---

## typoglycemia_attack
*Attempts to exploit a text processing vulnerability in LLMs that can cause incorrect responses by removing random characters from words.*

---

## ucar
*Probes an LLM's adherence to content restrictions when explicitly requested to ignore such filters.
It assesses the robustness of the LLM's content moderation systems against direct challenges.*
