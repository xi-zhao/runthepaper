# Lessons learned

1. The decisive numerical issue was not plotting but stable non-Hermitian
   linear algebra. QR-stabilized transfer products and conditioned OBC
   diagonalization were required before visual tuning became meaningful.
2. Scientific and visual acceptance must remain separate. The physical gates
   can all pass while exact pixels remain unrecoverable because seeds, state
   windows, grid details, and final artwork are unavailable.
3. A resumable batch state is essential for a 3200-realization ensemble.
   Completed batches must be keyed and applied exactly once.
4. Formal publication metadata can differ materially from the preprint. This
   case changed title at publication, so both identities are recorded.
5. Public packages should contain independently generated data and figures,
   not the internal source-reference assets used during audit.
