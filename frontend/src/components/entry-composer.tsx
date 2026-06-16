import { useState } from "react";
import {
  addCustomEntryChip,
  canAddCustomEntryChip,
  loadCustomEntryChips,
  normalizeCustomChip,
  removeCustomEntryChip,
} from "../lib/custom-entry-chips";
import {
  ENTRY_FIELD_LABEL,
  ENTRY_MAX_LENGTH,
  ENTRY_MOODS,
  ENTRY_PLACEHOLDER,
  ENTRY_QUICK_CHIPS,
} from "../lib/entry-prompts";
import { moodTone } from "../lib/mood";
import { WashiCard } from "./washi-card";

interface EntryComposerProps {
  onSubmit: (text: string, mood?: number) => Promise<void>;
}

export function EntryComposer({ onSubmit }: EntryComposerProps) {
  const [text, setText] = useState("");
  const [mood, setMood] = useState<number | undefined>();
  const [saving, setSaving] = useState(false);
  const [customChips, setCustomChips] = useState(loadCustomEntryChips);
  const [addingCustom, setAddingCustom] = useState(false);
  const [customDraft, setCustomDraft] = useState("");

  async function handleSubmit() {
    if (!text.trim() || saving) return;
    setSaving(true);
    try {
      await onSubmit(text.trim(), mood);
      setText("");
      setMood(undefined);
      setAddingCustom(false);
      setCustomDraft("");
    } finally {
      setSaving(false);
    }
  }

  function appendChip(chip: string) {
    setText((current) => {
      const trimmed = current.trim();
      let next = trimmed;
      if (!trimmed) {
        next = chip;
      } else if (
        !trimmed.endsWith(chip) &&
        !trimmed.split(/[,·]/).some((part) => part.trim() === chip)
      ) {
        next = `${trimmed}, ${chip}`;
      }
      return next.slice(0, ENTRY_MAX_LENGTH);
    });
  }

  function handleTextChange(value: string) {
    setText(value.slice(0, ENTRY_MAX_LENGTH));
  }

  function openCustomInput() {
    setAddingCustom(true);
  }

  function closeCustomInput() {
    setAddingCustom(false);
    setCustomDraft("");
  }

  function commitCustomChip() {
    const chip = normalizeCustomChip(customDraft);
    if (!chip) {
      closeCustomInput();
      return;
    }
    setCustomChips((current) => addCustomEntryChip(chip, current));
    appendChip(chip);
    closeCustomInput();
  }

  function handleCustomDraftKeyDown(key: string) {
    if (key === "Enter") {
      commitCustomChip();
      return;
    }
    if (key === "Escape") {
      closeCustomInput();
    }
  }

  function handleRemoveCustomChip(chip: string) {
    setCustomChips((current) => removeCustomEntryChip(chip, current));
  }

  const canSubmit = Boolean(text.trim()) && !saving;
  const canAddCustom = canAddCustomEntryChip(customChips);

  return (
    <WashiCard className="composer-shell" padded={false}>
      <p className="page-eyebrow composer-shell__head">новая запись</p>

      <div className="composer-body">
        <div className="composer-stack">
        <div className="composer-field">
          <textarea
            aria-label={ENTRY_FIELD_LABEL}
            className="composer-input"
            placeholder={ENTRY_PLACEHOLDER}
            maxLength={ENTRY_MAX_LENGTH}
            value={text}
            onChange={(e) => handleTextChange(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
                e.preventDefault();
                void handleSubmit();
              }
            }}
          />
        </div>

        <div className="composer-prompts" aria-label="Быстрые подсказки">
        <div className="composer-chip-row">
          {ENTRY_QUICK_CHIPS.map((chip) => (
            <button
              key={chip}
              type="button"
              aria-label={`Добавить: ${chip}`}
              className="composer-chip"
              onClick={() => appendChip(chip)}
            >
              {chip}
            </button>
          ))}
          {customChips.map((chip) => (
            <div key={chip} className="composer-chip-pill">
              <button
                type="button"
                aria-label={`Добавить: ${chip}`}
                className="composer-chip-pill__label"
                onClick={() => appendChip(chip)}
              >
                {chip}
              </button>
              <button
                type="button"
                aria-label={`Удалить подсказку: ${chip}`}
                className="composer-chip-pill__remove"
                onClick={() => handleRemoveCustomChip(chip)}
              >
                ×
              </button>
            </div>
          ))}
          {!addingCustom && canAddCustom && (
            <button
              type="button"
              aria-label="Добавить свою подсказку"
              className="composer-chip composer-chip--add"
              onClick={openCustomInput}
            >
              +
            </button>
          )}
        </div>

        {addingCustom && (
          <div className="composer-custom-form" role="group" aria-label="Новая подсказка">
            <input
              type="text"
              aria-label="Своя подсказка"
              className="composer-custom-input"
              placeholder="своя подсказка"
              value={customDraft}
              autoFocus
              onChange={(e) => setCustomDraft(e.target.value)}
              onKeyDown={(e) => handleCustomDraftKeyDown(e.key)}
            />
            <button
              type="button"
              aria-label="Сохранить подсказку"
              className="composer-custom-action composer-custom-action--save"
              onClick={commitCustomChip}
            >
              ✓
            </button>
            <button
              type="button"
              aria-label="Отменить"
              className="composer-custom-action composer-custom-action--cancel"
              onClick={closeCustomInput}
            >
              ×
            </button>
          </div>
        )}
        </div>

        <div className="composer-moods">
          <p className="composer-mood-label">Как было?</p>
          <div className="composer-mood-row" role="group" aria-label="Настроение">
            {ENTRY_MOODS.map((item) => {
              const active = mood === item.value;
              return (
                <button
                  key={item.value}
                  type="button"
                  aria-pressed={active}
                  aria-label={"title" in item ? item.title : item.label}
                  className={active ? "composer-mood composer-mood--active" : "composer-mood"}
                  onClick={() => setMood(active ? undefined : item.value)}
                >
                  <span
                    className="composer-mood-dot"
                    style={{ background: moodTone(item.value) }}
                    aria-hidden
                  />
                  {item.label}
                </button>
              );
            })}
          </div>
        </div>

        <div className="composer-actions">
          <button
            type="button"
            disabled={!canSubmit}
            className="composer-submit"
            onClick={() => void handleSubmit()}
          >
            {saving ? "Сохраняю…" : "Записать"}
          </button>
          <p className="composer-hint">⌘↵</p>
        </div>
        </div>
      </div>
    </WashiCard>
  );
}
