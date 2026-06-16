import { useEffect, useRef, useState, type CSSProperties } from "react";
import type { Entry, TagCategory } from "../api/types";
import type { EntryMutations } from "../hooks/use-entry-mutations";
import { categoryColor } from "../lib/category-colors";
import { ENTRY_CATEGORIES } from "../lib/entry-categories";
import { categoryLabel } from "../lib/category-labels";
import { ENTRY_MOODS } from "../lib/entry-prompts";
import { moodTone } from "../lib/mood";

interface EntryControlsProps {
  entry: Entry;
  mutations: EntryMutations;
}

function containsNode(container: HTMLElement | null, target: EventTarget | null): boolean {
  return target instanceof Node && container?.contains(target) === true;
}

function CrossIcon() {
  return (
    <svg viewBox="0 0 16 16" width="12" height="12" aria-hidden>
      <path
        d="M4.25 4.25l7.5 7.5M11.75 4.25l-7.5 7.5"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.3"
        strokeLinecap="round"
      />
    </svg>
  );
}

export function EntryControls({ entry, mutations }: EntryControlsProps) {
  const [categoryOpen, setCategoryOpen] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const catRef = useRef<HTMLDivElement>(null);
  const category = entry.tags[0]?.category ?? "work";
  const busy = mutations.updateEntry.isPending || mutations.deleteEntry.isPending;

  useEffect(() => {
    if (!categoryOpen) return;

    const onPointer = (event: MouseEvent | TouchEvent) => {
      if (containsNode(catRef.current, event.target)) return;
      setCategoryOpen(false);
    };

    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") setCategoryOpen(false);
    };

    document.addEventListener("mousedown", onPointer);
    document.addEventListener("touchstart", onPointer);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onPointer);
      document.removeEventListener("touchstart", onPointer);
      document.removeEventListener("keydown", onKey);
    };
  }, [categoryOpen]);

  function toggleCategoryMenu() {
    if (busy) return;
    setCategoryOpen((open) => !open);
  }

  function handleCategoryChange(next: TagCategory) {
    setCategoryOpen(false);
    if (next === category || busy) return;
    mutations.updateEntry.mutate({ id: entry.id, patch: { category: next } });
  }

  function handleMoodChange(next: number) {
    if (entry.mood === next || busy) return;
    mutations.updateEntry.mutate({ id: entry.id, patch: { mood: next } });
  }

  function handleDeleteClick() {
    if (!confirmDelete) {
      setConfirmDelete(true);
      return;
    }
    mutations.deleteEntry.mutate(entry.id);
  }

  function cancelDelete() {
    setConfirmDelete(false);
  }

  return (
    <div className="entry-toolbar" aria-label="Управление записью">
      <div className="entry-toolbar__cat" ref={catRef}>
        <button
          type="button"
          className="entry-cat-toggle"
          aria-expanded={categoryOpen}
          aria-haspopup="listbox"
          aria-label={`Категория: ${categoryLabel(category)}`}
          disabled={busy}
          style={{ "--entry-cat-accent": categoryColor(category) } as CSSProperties}
          onClick={toggleCategoryMenu}
        >
          <span className="entry-cat-toggle__dot" aria-hidden />
          <span>{categoryLabel(category)}</span>
          <span className="entry-cat-toggle__chev" aria-hidden />
        </button>

        {categoryOpen && (
          <div className="entry-cat-menu" role="listbox" aria-label="Выбор категории">
            {ENTRY_CATEGORIES.map((item) => {
              const active = category === item;
              return (
                <button
                  key={item}
                  type="button"
                  role="option"
                  aria-selected={active}
                  disabled={busy}
                  className={active ? "entry-cat-menu__item entry-cat-menu__item--active" : "entry-cat-menu__item"}
                  style={
                    active
                      ? ({ "--entry-cat-accent": categoryColor(item) } as CSSProperties)
                      : undefined
                  }
                  onClick={() => handleCategoryChange(item)}
                >
                  <span className="entry-cat-menu__dot" aria-hidden />
                  {categoryLabel(item)}
                </button>
              );
            })}
          </div>
        )}
      </div>

      <div className="entry-toolbar__moods entry-mood-rail" role="group" aria-label="Настроение записи">
        {ENTRY_MOODS.map((item) => {
          const active = entry.mood === item.value;
          return (
            <button
              key={item.value}
              type="button"
              aria-pressed={active}
              aria-label={item.label}
              disabled={busy}
              title={item.label}
              className={active ? "entry-mood-chip entry-mood-chip--active" : "entry-mood-chip"}
              onClick={() => handleMoodChange(item.value)}
            >
              <span
                className="entry-mood-chip__dot"
                style={{ background: moodTone(item.value) }}
                aria-hidden
              />
            </button>
          );
        })}
      </div>

      <div className="entry-toolbar__delete">
        {confirmDelete ? (
          <div className="entry-delete-confirm" role="group" aria-label="Подтверждение удаления">
            <button
              type="button"
              className="entry-delete-confirm__yes"
              aria-label="Подтвердить удаление"
              disabled={busy}
              onClick={handleDeleteClick}
            >
              ✓
            </button>
            <button
              type="button"
              className="entry-delete-confirm__no"
              aria-label="Отменить удаление"
              disabled={busy}
              onClick={cancelDelete}
            >
              ×
            </button>
          </div>
        ) : (
          <button
            type="button"
            className="entry-toolbar__delete-btn"
            aria-label="Удалить запись"
            disabled={busy}
            onClick={handleDeleteClick}
          >
            <CrossIcon />
          </button>
        )}
      </div>
    </div>
  );
}
