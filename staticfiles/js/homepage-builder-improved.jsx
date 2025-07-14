// Improved Homepage Builder with better drag-and-drop UX and state isolation
const { useState, useEffect, useCallback, useReducer, useMemo } = React;
const { DragDropContext, Droppable, Draggable } = ReactBeautifulDnd;

// State management with useReducer for complex state
const blockReducer = (state, action) => {
  switch (action.type) {
    case 'SET_BLOCKS':
      return { ...state, blocks: action.payload };
    case 'ADD_BLOCK':
      return { ...state, blocks: [...state.blocks, action.payload] };
    case 'UPDATE_BLOCK':
      return {
        ...state,
        blocks: state.blocks.map(block =>
          block.id === action.payload.id ? { ...block, ...action.payload.updates } : block
        )
      };
    case 'DELETE_BLOCK':
      return {
        ...state,
        blocks: state.blocks.filter(block => block.id !== action.payload)
      };
    case 'REORDER_BLOCKS':
      return { ...state, blocks: action.payload };
    case 'SET_SELECTED':
      return { ...state, selectedBlock: action.payload };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    default:
      return state;
  }
};

// Block type definitions with enhanced metadata
const blockTypes = {
  hero_banner: { 
    name: "Hero Banner", 
    icon: "🖼️", 
    category: "Layout",
    description: "Large banner with image and call-to-action"
  },
  product_grid: { 
    name: "Product Grid", 
    icon: "🛍️", 
    category: "Products",
    description: "Grid layout of products"
  },
  featured_products: { 
    name: "Featured Products", 
    icon: "⭐", 
    category: "Products",
    description: "Highlighted product showcase"
  },
  testimonials: { 
    name: "Testimonials", 
    icon: "💬", 
    category: "Social Proof",
    description: "Customer reviews and testimonials"
  },
  text_block: { 
    name: "Text Block", 
    icon: "📝", 
    category: "Content",
    description: "Rich text content section"
  },
  image_gallery: { 
    name: "Image Gallery", 
    icon: "🖼️", 
    category: "Media",
    description: "Collection of images"
  },
  video_embed: { 
    name: "Video Embed", 
    icon: "🎬", 
    category: "Media",
    description: "Embedded video content"
  },
  trust_badges: { 
    name: "Trust Badges", 
    icon: "🛡️", 
    category: "Social Proof",
    description: "Trust and security badges"
  },
  contact_form: { 
    name: "Contact Form", 
    icon: "📧", 
    category: "Interaction",
    description: "Customer contact form"
  },
  tag_collection: { 
    name: "Tag Collection", 
    icon: "🏷️", 
    category: "Navigation",
    description: "Product tag navigation"
  },
};

// Custom hooks for better state isolation
const useAPI = () => {
  const [csrfToken, setCsrfToken] = useState('');

  useEffect(() => {
    const tokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
    if (tokenElement) {
      setCsrfToken(tokenElement.value);
    }
  }, []);

  const apiCall = useCallback(async (url, options = {}) => {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API call failed: ${response.statusText}`);
    }

    return response.json();
  }, [csrfToken]);

  return { apiCall };
};

const useBlockOperations = (dispatch) => {
  const { apiCall } = useAPI();

  const createBlock = useCallback(async (blockType, title) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    try {
      const data = await apiCall(`/stores/${window.storeSlug}/homepage/blocks/create/`, {
        method: 'POST',
        body: JSON.stringify({ block_type: blockType, title }),
      });

      if (data.status === 'success') {
        const newBlock = {
          id: data.block_id,
          block_type: data.block_type,
          title: data.title,
          content: '',
          order: data.order,
          is_active: true,
          configuration: {},
        };
        dispatch({ type: 'ADD_BLOCK', payload: newBlock });
        return newBlock;
      }
      throw new Error(data.message || 'Failed to create block');
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  }, [apiCall, dispatch]);

  const updateBlock = useCallback(async (blockId, updates) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    try {
      const data = await apiCall(`/stores/${window.storeSlug}/homepage/blocks/${blockId}/update/`, {
        method: 'POST',
        body: JSON.stringify(updates),
      });

      if (data.status === 'success') {
        dispatch({ type: 'UPDATE_BLOCK', payload: { id: blockId, updates } });
      } else {
        throw new Error(data.message || 'Failed to update block');
      }
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  }, [apiCall, dispatch]);

  const deleteBlock = useCallback(async (blockId) => {
    if (!confirm('Are you sure you want to delete this block?')) return;

    dispatch({ type: 'SET_LOADING', payload: true });
    try {
      const data = await apiCall(`/stores/${window.storeSlug}/homepage/blocks/${blockId}/delete/`, {
        method: 'POST',
      });

      if (data.status === 'success') {
        dispatch({ type: 'DELETE_BLOCK', payload: blockId });
      } else {
        throw new Error(data.message || 'Failed to delete block');
      }
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  }, [apiCall, dispatch]);

  const saveOrder = useCallback(async (blocks) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    try {
      const data = await apiCall(`/stores/${window.storeSlug}/homepage/blocks/reorder/`, {
        method: 'POST',
        body: JSON.stringify({ block_order: blocks.map(block => block.id) }),
      });

      if (data.status === 'success') {
        return true;
      }
      throw new Error(data.message || 'Failed to save block order');
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  }, [apiCall, dispatch]);

  return { createBlock, updateBlock, deleteBlock, saveOrder };
};

// Enhanced Block Editor Component
const BlockEditor = React.memo(({ block, onUpdate, onClose }) => {
  const [localState, setLocalState] = useState({
    title: block.title || '',
    content: block.content || '',
    configuration: block.configuration || {}
  });

  const [hasChanges, setHasChanges] = useState(false);

  useEffect(() => {
    const hasChanged = 
      localState.title !== block.title ||
      localState.content !== block.content ||
      JSON.stringify(localState.configuration) !== JSON.stringify(block.configuration);
    setHasChanges(hasChanged);
  }, [localState, block]);

  const handleSave = useCallback(() => {
    onUpdate(block.id, localState);
    setHasChanges(false);
  }, [block.id, localState, onUpdate]);

  const updateConfig = useCallback((key, value) => {
    setLocalState(prev => ({
      ...prev,
      configuration: { ...prev.configuration, [key]: value }
    }));
  }, []);

  const renderConfigOptions = useMemo(() => {
    const { configuration } = localState;
    
    switch (block.block_type) {
      case 'hero_banner':
        return (
          <>
            <ConfigField
              label="Image URL"
              value={configuration.image_url || ''}
              onChange={(value) => updateConfig('image_url', value)}
            />
            <ConfigField
              label="Button Text"
              value={configuration.button_text || ''}
              onChange={(value) => updateConfig('button_text', value)}
            />
            <ConfigField
              label="Button URL"
              value={configuration.button_url || ''}
              onChange={(value) => updateConfig('button_url', value)}
            />
            <ConfigSelect
              label="Height"
              value={configuration.height || 'lg'}
              options={[
                { value: 'sm', label: 'Small' },
                { value: 'md', label: 'Medium' },
                { value: 'lg', label: 'Large' },
                { value: 'xl', label: 'Extra Large' }
              ]}
              onChange={(value) => updateConfig('height', value)}
            />
          </>
        );
      case 'product_grid':
        return (
          <>
            <ConfigField
              label="Products per row"
              type="number"
              value={configuration.columns || 3}
              onChange={(value) => updateConfig('columns', parseInt(value))}
            />
            <ConfigField
              label="Max products to show"
              type="number"
              value={configuration.limit || 12}
              onChange={(value) => updateConfig('limit', parseInt(value))}
            />
          </>
        );
      case 'contact_form':
        return (
          <>
            <ConfigField
              label="Background Color"
              type="color"
              value={configuration.background_color || '#ffffff'}
              onChange={(value) => updateConfig('background_color', value)}
            />
            <ConfigField
              label="Contact Form ID"
              type="number"
              value={configuration.contact_form_id || ''}
              onChange={(value) => updateConfig('contact_form_id', value)}
            />
          </>
        );
      default:
        return <p className="text-theme-secondary">No specific configuration options for this block type.</p>;
    }
  }, [block.block_type, localState.configuration, updateConfig]);

  return (
    <div className="bg-card p-6 rounded-lg shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-theme">
          Edit {blockTypes[block.block_type]?.name || 'Block'}
        </h3>
        {hasChanges && (
          <span className="text-sm text-orange-600 bg-orange-100 px-2 py-1 rounded">
            Unsaved changes
          </span>
        )}
      </div>
      
      <div className="space-y-4">
        <ConfigField
          label="Title"
          value={localState.title}
          onChange={(value) => setLocalState(prev => ({ ...prev, title: value }))}
        />
        
        <div>
          <label className="block text-theme-secondary mb-2 font-medium">Content</label>
          <textarea
            value={localState.content}
            onChange={(e) => setLocalState(prev => ({ ...prev, content: e.target.value }))}
            className="w-full px-3 py-2 border border-theme-secondary rounded-md focus:ring-2 focus:ring-primary focus:border-transparent"
            rows="4"
            placeholder="Enter block content..."
          />
        </div>
        
        <div>
          <h4 className="font-bold mb-3 text-theme">Configuration</h4>
          <div className="space-y-3">
            {renderConfigOptions}
          </div>
        </div>
      </div>
      
      <div className="flex justify-between mt-6 pt-4 border-t border-theme-secondary">
        <button
          onClick={onClose}
          className="px-4 py-2 text-theme border border-theme-secondary rounded-md hover:bg-theme-secondary hover:bg-opacity-10 transition-colors"
        >
          Cancel
        </button>
        <button
          onClick={handleSave}
          disabled={!hasChanges}
          className="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-hover disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Save Changes
        </button>
      </div>
    </div>
  );
});

// Reusable configuration field components
const ConfigField = ({ label, value, onChange, type = 'text', placeholder }) => (
  <div>
    <label className="block text-theme-secondary mb-1 font-medium text-sm">{label}</label>
    <input
      type={type}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      className="w-full px-3 py-2 border border-theme-secondary rounded-md focus:ring-2 focus:ring-primary focus:border-transparent text-sm"
    />
  </div>
);

const ConfigSelect = ({ label, value, onChange, options }) => (
  <div>
    <label className="block text-theme-secondary mb-1 font-medium text-sm">{label}</label>
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full px-3 py-2 border border-theme-secondary rounded-md focus:ring-2 focus:ring-primary focus:border-transparent text-sm"
    >
      {options.map(option => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  </div>
);

// Enhanced Block Item Component
const BlockItem = React.memo(({ block, index, onEdit, onToggle, onDelete }) => {
  const blockInfo = blockTypes[block.block_type] || { name: 'Unknown', icon: '📦' };
  
  return (
    <div className="bg-theme border border-theme-secondary rounded-lg p-4 flex items-center justify-between hover:shadow-md transition-shadow">
      <div className="flex items-center space-x-3">
        <div className="text-2xl">{blockInfo.icon}</div>
        <div className="flex-1">
          <h3 className="font-medium text-theme">
            {block.title || blockInfo.name}
          </h3>
          <p className="text-sm text-theme-secondary">
            {blockInfo.name} • Order: {index + 1}
          </p>
        </div>
      </div>
      
      <div className="flex items-center space-x-3">
        <label className="inline-flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={block.is_active}
            onChange={() => onToggle(block.id, !block.is_active)}
            className="form-checkbox h-4 w-4 text-primary rounded focus:ring-primary"
          />
          <span className="ml-2 text-sm text-theme-secondary">Active</span>
        </label>
        
        <button
          onClick={() => onEdit(block)}
          className="text-primary hover:text-primary-hover text-sm font-medium transition-colors"
        >
          Edit
        </button>
        
        <button
          onClick={() => onDelete(block.id)}
          className="text-red-500 hover:text-red-700 text-sm font-medium transition-colors"
        >
          Delete
        </button>
      </div>
    </div>
  );
});

// Main Homepage Builder Component
function HomepageBuilder() {
  const initialState = {
    blocks: [],
    selectedBlock: null,
    loading: false,
    error: null
  };

  const [state, dispatch] = useReducer(blockReducer, initialState);
  const [addingBlock, setAddingBlock] = useState(false);
  const [newBlockType, setNewBlockType] = useState('');
  
  const { createBlock, updateBlock, deleteBlock, saveOrder } = useBlockOperations(dispatch);

  // Load initial blocks
  useEffect(() => {
    const builderElement = document.getElementById('homepage-builder');
    if (builderElement?.dataset.blocks) {
      try {
        const loadedBlocks = JSON.parse(builderElement.dataset.blocks);
        dispatch({ type: 'SET_BLOCKS', payload: loadedBlocks });
      } catch (e) {
        dispatch({ type: 'SET_ERROR', payload: 'Failed to load blocks' });
      }
    }
  }, []);

  // Enhanced drag end handler
  const handleDragEnd = useCallback((result) => {
    if (!result.destination) return;

    const items = Array.from(state.blocks);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);

    const updatedItems = items.map((item, index) => ({
      ...item,
      order: index,
    }));

    dispatch({ type: 'REORDER_BLOCKS', payload: updatedItems });
  }, [state.blocks]);

  const handleAddBlock = useCallback(async () => {
    if (!newBlockType) return;

    try {
      const newBlock = await createBlock(newBlockType, `New ${blockTypes[newBlockType].name}`);
      dispatch({ type: 'SET_SELECTED', payload: newBlock });
      setAddingBlock(false);
      setNewBlockType('');
    } catch (err) {
      dispatch({ type: 'SET_ERROR', payload: err.message });
    }
  }, [newBlockType, createBlock]);

  const handleSaveOrder = useCallback(async () => {
    try {
      await saveOrder(state.blocks);
      alert('Homepage layout saved successfully!');
    } catch (err) {
      alert('Failed to save layout: ' + err.message);
    }
  }, [state.blocks, saveOrder]);

  // Connect save button
  useEffect(() => {
    const saveButton = document.getElementById('save-changes-btn');
    if (saveButton) {
      saveButton.addEventListener('click', handleSaveOrder);
      return () => saveButton.removeEventListener('click', handleSaveOrder);
    }
  }, [handleSaveOrder]);

  // Group block types by category
  const blockTypesByCategory = useMemo(() => {
    const grouped = {};
    Object.entries(blockTypes).forEach(([key, value]) => {
      const category = value.category || 'Other';
      if (!grouped[category]) grouped[category] = [];
      grouped[category].push({ key, ...value });
    });
    return grouped;
  }, []);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Block List */}
      <div className="lg:col-span-2">
        <div className="bg-card p-6 rounded-lg shadow editor-panel">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-theme">Homepage Blocks</h2>
            <button
              onClick={() => setAddingBlock(!addingBlock)}
              className="bg-primary hover:bg-primary-hover text-white px-4 py-2 rounded-md transition-colors"
            >
              {addingBlock ? 'Cancel' : 'Add Block'}
            </button>
          </div>

          {/* Add Block Form */}
          {addingBlock && (
            <div className="mb-6 p-4 border border-theme-secondary rounded-lg bg-theme-secondary bg-opacity-5">
              <h3 className="text-lg font-bold mb-4 text-theme">Add New Block</h3>
              
              {Object.entries(blockTypesByCategory).map(([category, blocks]) => (
                <div key={category} className="mb-4">
                  <h4 className="font-medium text-theme-secondary mb-2">{category}</h4>
                  <div className="grid grid-cols-2 gap-2">
                    {blocks.map(({ key, name, icon, description }) => (
                      <button
                        key={key}
                        onClick={() => setNewBlockType(key)}
                        className={`p-3 text-left border rounded-md transition-colors ${
                          newBlockType === key
                            ? 'border-primary bg-primary bg-opacity-10'
                            : 'border-theme-secondary hover:border-primary'
                        }`}
                      >
                        <div className="flex items-center space-x-2">
                          <span className="text-lg">{icon}</span>
                          <div>
                            <div className="font-medium text-sm">{name}</div>
                            <div className="text-xs text-theme-secondary">{description}</div>
                          </div>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              ))}
              
              <button
                onClick={handleAddBlock}
                disabled={!newBlockType || state.loading}
                className="bg-primary hover:bg-primary-hover text-white px-4 py-2 rounded-md disabled:opacity-50 transition-colors"
              >
                {state.loading ? 'Adding...' : 'Add Block'}
              </button>
            </div>
          )}

          {/* Error Message */}
          {state.error && (
            <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
              {state.error}
            </div>
          )}

          {/* Block List */}
          {state.blocks.length === 0 ? (
            <div className="text-center py-12 text-theme-secondary">
              <div className="text-4xl mb-4">📦</div>
              <p className="text-lg mb-2">No blocks added yet</p>
              <p>Click "Add Block" to start building your homepage.</p>
            </div>
          ) : (
            <DragDropContext onDragEnd={handleDragEnd}>
              <Droppable droppableId="blocks">
                {(provided, snapshot) => (
                  <div
                    {...provided.droppableProps}
                    ref={provided.innerRef}
                    className={`space-y-3 ${snapshot.isDraggingOver ? 'bg-primary bg-opacity-5 rounded-lg p-2' : ''}`}
                  >
                    {state.blocks.map((block, index) => (
                      <Draggable
                        key={block.id.toString()}
                        draggableId={block.id.toString()}
                        index={index}
                      >
                        {(provided, snapshot) => (
                          <div
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            className={`${snapshot.isDragging ? 'shadow-lg scale-105' : ''} transition-transform`}
                          >
                            <BlockItem
                              block={block}
                              index={index}
                              onEdit={(block) => dispatch({ type: 'SET_SELECTED', payload: block })}
                              onToggle={(id, isActive) => updateBlock(id, { is_active: isActive })}
                              onDelete={deleteBlock}
                            />
                          </div>
                        )}
                      </Draggable>
                    ))}
                    {provided.placeholder}
                  </div>
                )}
              </Droppable>
            </DragDropContext>
          )}
        </div>
      </div>

      {/* Block Editor */}
      <div className="lg:col-span-1">
        <div className="bg-card rounded-lg shadow editor-panel sticky top-6">
          {state.selectedBlock ? (
            <BlockEditor
              block={state.selectedBlock}
              onUpdate={updateBlock}
              onClose={() => dispatch({ type: 'SET_SELECTED', payload: null })}
            />
          ) : (
            <div className="p-6 text-center text-theme-secondary">
              <div className="text-4xl mb-4">✏️</div>
              <p className="text-lg mb-2">Select a block to edit</p>
              <p>Click on any block to configure its content and settings.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Render the component
ReactDOM.render(<HomepageBuilder />, document.getElementById('homepage-builder'));