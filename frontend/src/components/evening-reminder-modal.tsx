import { useEffect, useRef } from "react";
import { EntryComposer } from "./entry-composer";
import { WashiCard } from "./washi-card";

interface EveningReminderModalProps {
  open: boolean;
  onDismiss: () => void;
  onDisable: () => void;
  onSubmit: (text: string, mood?: number) => Promise<void>;
}

export function EveningReminderModal({
  open,
  onDismiss,
  onDisable,
  onSubmit,
}: EveningReminderModalProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) {
      return;
    }
    if (open && !dialog.open) {
      dialog.showModal();
    } else if (!open && dialog.open) {
      dialog.close();
    }
  }, [open]);

  return (
    <dialog
      ref={dialogRef}
      className="evening-reminder-dialog"
      role="dialog"
      aria-modal="true"
      aria-labelledby="evening-reminder-title"
      onCancel={(event) => {
        event.preventDefault();
        onDismiss();
      }}
    >
      <WashiCard className="evening-reminder-dialog__card">
        <header className="evening-reminder-dialog__header">
          <h2 id="evening-reminder-title" className="evening-reminder-dialog__title">
            Что сделал сегодня?
          </h2>
          <p className="evening-reminder-dialog__subtitle">
            Одна строка — и день не пропадёт из истории.
          </p>
        </header>

        <EntryComposer onSubmit={onSubmit} />

        <footer className="evening-reminder-dialog__footer">
          <button type="button" className="evening-reminder-dialog__action" onClick={onDismiss}>
            Позже
          </button>
          <button
            type="button"
            className="evening-reminder-dialog__action evening-reminder-dialog__action--muted"
            onClick={onDisable}
          >
            Не напоминать
          </button>
        </footer>
      </WashiCard>
    </dialog>
  );
}
