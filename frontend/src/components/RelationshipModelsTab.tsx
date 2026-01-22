import { useStore } from '../store';

interface RelationshipModelsTabProps {
  relationshipId: string;
}

export function RelationshipModelsTab({ relationshipId }: RelationshipModelsTabProps) {
  const { relationships } = useStore();
  const relationship = relationships[relationshipId];

  if (!relationship) return null;

  const hasModels = relationship.realized_by.length > 0;

  return (
    <div className="models-tab">
      {/* Realized By Models */}
      <div className="model-section">
        <div className="model-section-header">
          <span className="model-section-icon model-section-icon-gold">&#9670;</span>
          <span className="model-section-title">Realized By</span>
          <span className="model-section-count">{relationship.realized_by.length}</span>
        </div>
        {hasModels ? (
          <div className="model-list">
            {relationship.realized_by.map((model) => (
              <div key={model} className="model-item model-item-gold">
                <span className="model-item-name">{model}</span>
              </div>
            ))}
          </div>
        ) : (
          <div className="model-empty">
            No models realize this relationship
            <div className="model-empty-hint">
              Add <code>meta.realizes: {relationship.from_concept}:{relationship.verb}:{relationship.to_concept}</code> to a model
            </div>
          </div>
        )}
      </div>

      {/* Help text */}
      <div className="model-help">
        <div className="model-help-title">How to realize relationships</div>
        <div className="model-help-text">
          Add the <code>meta.realizes</code> key to your dbt model's YAML:
        </div>
        <pre className="model-help-code">
{`models:
  - name: my_model
    meta:
      realizes:
        - ${relationship.from_concept}:${relationship.verb}:${relationship.to_concept}`}
        </pre>
      </div>
    </div>
  );
}
