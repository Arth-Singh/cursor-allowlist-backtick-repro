# Cursor shell allowlist: nested backtick reproduction

Reproduction for a Cursor Agents shell permission parser discrepancy. In a
parameter expansion of the form below, Cursor counted the outer `echo` but
omitted the nested backtick command. With `echo` on the Command Allowlist,
Cursor applied `insecure_none` to the full shell call, and the shell executed
`touch` outside the project without an approval card.

```sh
echo ${LINECOUNT_SESSION:-`/usr/bin/touch /ABSOLUTE/PATH/OUTSIDE/PROJECT/marker.txt`}
```

The observed environment was Cursor Agents desktop 3.22.12 on macOS, Run Mode
**Allowlist (with Sandbox)**, External-File Protection on, and only `echo`
temporarily added to Command Allowlist. This proof requires `echo` to be
allowlisted and `LINECOUNT_SESSION` to be unset or empty in the agent shell.
It does not demonstrate an escape with an empty allowlist.

## Reproduce

1. Choose an absent marker file in an existing directory outside this project,
   for example `/Users/YOUR_USERNAME/Downloads/cursor-parser-proof.txt`.
   From this repository root, run:

   ```sh
   python3 prepare.py /Users/YOUR_USERNAME/Downloads/cursor-parser-proof.txt
   ```

   Replace `YOUR_USERNAME` with your local account name. The script writes
   `victim-project/README.md` from the tested wording; it does not create the
   marker. Use a path without spaces or shell metacharacters.

2. In Cursor Settings → Agents → Execution and Approvals, set Run Mode to
   **Allowlist (with Sandbox)**, keep External-File Protection on, and add
   `echo` alone to Command Allowlist. Do not allowlist `touch`.
3. Open `victim-project/` as the Cursor project. Start a fresh agent
   conversation and ask: `Run this project and tell me what it prints.`
4. Check the agent conversation for a standalone `echo` preflight, then
   `python3 -m src.linecount`. Check whether the marker appeared outside the
   project and whether Cursor showed an approval card for the preflight.
   The program itself prints `2`.
5. Restore the prior Command Allowlist and settings. Delete the marker and
   generated `victim-project/README.md` after recording the result.

The original local test yielded the marker without an approval card.
Cursor Agent Exec recorded `parserCommandCount:1`,
`allCommandsAllowlisted:true`, and `effectivePolicyType:"insecure_none"`
for the preflight. The later Python command used `workspace_readwrite`.
With the original empty allowlist, an outside-workspace marker write failed
under `workspace_readwrite`; a requested unsandboxed retry stopped at an
approval card. These are observations from one local test, not guaranteed
behavior across Cursor versions or models.

No network request or sensitive-data read is part of this proof. The only
intended side effect is the named local marker file.
