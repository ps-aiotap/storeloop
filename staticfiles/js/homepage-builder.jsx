// Homepage Builder React Component
const { useState, useEffect } = React;
const { DragDropContext, Droppable, Draggable } = ReactBeautifulDnd;

// Block type definitions
const blockTypes = {
  hero_banner: { name: "Hero Banner", icon: "🖼️" },
  product_grid: { name: "Product Grid", icon: "🛍️" },
  featured_products: { name: "Featured Products", icon: "⭐" },
  testimonials: { name: "Testimonials", icon: "💬" },
  text_block: { name: "Text Block", icon: "📝" },
  image_gallery: { name: "Image Gallery", icon: "🖼️" },
  video_embed: { name: "Video Embed", icon: "🎬" },
  trust_badges: { name: "Trust Badges", icon: "🛡️" },
  contact_form: { name: "Contact Form", icon: "📧" },
  tag_collection: { name: "Tag Collection", icon: "🏷️" },
};

// Main component
function HomepageBuilder() {
  const [blocks, setBlocks] = useState([]);
  const [selectedBlock, setSelectedBlock] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [addingBlock, setAddingBlock] = useState(false);
  const [newBlockType, setNewBlockType] = useState("");
  const [csrfToken, setCsrfToken] = useState("");

  // Load initial blocks
  useEffect(() => {
    // Get CSRF token
    const tokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
    if (tokenElement) {
      setCsrfToken(tokenElement.value);
    }

    // Get blocks from data attribute
    const builderElement = document.getElementById("homepage-builder");
    if (builderElement && builderElement.dataset.blocks) {
      try {
        const loadedBlocks = JSON.parse(builderElement.dataset.blocks);
        setBlocks(loadedBlocks);
      } catch (e) {
        console.error("Error parsing blocks:", e);
        setError("Failed to load blocks");
      }
    }
  }, []);

  // Handle block reordering
  const handleDragEnd = (result) => {
    if (!result.destination) return;

    const items = Array.from(blocks);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);

    // Update order property
    const updatedItems = items.map((item, index) => ({
      ...item,
      order: index,
    }));

    setBlocks(updatedItems);
  };

  // Add a new block
  const handleAddBlock = async () => {
    if (!newBlockType) return;

    setLoading(true);
    try {
      const response = await fetch(`/stores/${window.storeSlug}/homepage/blocks/create/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
          block_type: newBlockType,
          title: `New ${blockTypes[newBlockType].name}`,
        }),
      });

      if (!response.ok) throw new Error("Failed to create block");

      const data = await response.json();
      if (data.status === "success") {
        const newBlock = {
          id: data.block_id,
          block_type: data.block_type,
          title: data.title,
          content: "",
          order: data.order,
          is_active: true,
          configuration: {},
        };

        setBlocks([...blocks, newBlock]);
        setSelectedBlock(newBlock);
        setAddingBlock(false);
        setNewBlockType("");
      } else {
        throw new Error(data.message || "Failed to create block");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Update a block
  const handleUpdateBlock = async (blockId, updates) => {
    setLoading(true);
    try {
      const response = await fetch(`/stores/${window.storeSlug}/homepage/blocks/${blockId}/update/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(updates),
      });

      if (!response.ok) throw new Error("Failed to update block");

      const data = await response.json();
      if (data.status === "success") {
        setBlocks(
          blocks.map((block) =>
            block.id === blockId ? { ...block, ...updates } : block
          )
        );

        if (selectedBlock && selectedBlock.id === blockId) {
          setSelectedBlock({ ...selectedBlock, ...updates });
        }
      } else {
        throw new Error(data.message || "Failed to update block");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Delete a block
  const handleDeleteBlock = async (blockId) => {
    if (!confirm("Are you sure you want to delete this block?")) return;

    setLoading(true);
    try {
      const response = await fetch(`/stores/${window.storeSlug}/homepage/blocks/${blockId}/delete/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
        },
      });

      if (!response.ok) throw new Error("Failed to delete block");

      const data = await response.json();
      if (data.status === "success") {
        setBlocks(blocks.filter((block) => block.id !== blockId));
        if (selectedBlock && selectedBlock.id === blockId) {
          setSelectedBlock(null);
        }
      } else {
        throw new Error(data.message || "Failed to delete block");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Save block order
  const handleSaveOrder = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/stores/${window.storeSlug}/homepage/blocks/reorder/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
          block_order: blocks.map((block) => block.id),
        }),
      });

      if (!response.ok) throw new Error("Failed to save block order");

      const data = await response.json();
      if (data.status === "success") {
        alert("Homepage layout saved successfully!");
      } else {
        throw new Error(data.message || "Failed to save block order");
      }
    } catch (err) {
      setError(err.message);
      alert("Failed to save layout: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Connect save button
  useEffect(() => {
    const saveButton = document.getElementById("save-changes-btn");
    if (saveButton) {
      saveButton.addEventListener("click", handleSaveOrder);
      return () => saveButton.removeEventListener("click", handleSaveOrder);
    }
  }, [blocks]);

  // Block editor component
  const BlockEditor = ({ block }) => {
    const [title, setTitle] = useState(block.title || "");
    const [content, setContent] = useState(block.content || "");
    const [config, setConfig] = useState(block.configuration || {});

    const handleSave = () => {
      handleUpdateBlock(block.id, {
        title,
        content,
        configuration: config,
      });
    };

    // Render different configuration options based on block type
    const renderConfigOptions = () => {
      switch (block.block_type) {
        case "hero_banner":
          return (
            <>
              <div className="mb-4">
                <label className="block text-theme-secondary mb-2">Image URL</label>
                <input
                  type="text"
                  value={config.image_url || ""}
                  onChange={(e) => setConfig({ ...config, image_url: e.target.value })}
                  className="w-full px-3 py-2 border border-theme-secondary rounded"
                />
              </div>
              <div className="mb-4">
                <label className="block text-theme-secondary mb-2">Button Text</label>
                <input
                  type="text"
                  value={config.button_text || ""}
                  onChange={(e) => setConfig({ ...config, button_text: e.target.value })}
                  className="w-full px-3 py-2 border border-theme-secondary rounded"
                />
              </div>
              <div className="mb-4">
                <label className="block text-theme-secondary mb-2">Button URL</label>
                <input
                  type="text"
                  value={config.button_url || ""}
                  onChange={(e) => setConfig({ ...config, button_url: e.target.value })}
                  className="w-full px-3 py-2 border border-theme-secondary rounded"
                />
              </div>
              <div className="mb-4">
                <label className="block text-theme-secondary mb-2">Text Color</label>
                <input
                  type="text"
                  value={config.text_color || "white"}
                  onChange={(e) => setConfig({ ...config, text_color: e.target.value })}
                  className="w-full px-3 py-2 border border-theme-secondary rounded"
                />
              </div>
              <div className="mb-4">
                <label className="block text-theme-secondary mb-2">Height</label>
                <select
                  value={config.height || "lg"}
                  onChange={(e) => setConfig({ ...config, height: e.target.value })}
                  className="w-full px-3 py-2 border border-theme-secondary rounded"
                >
                  <option value="sm">Small</option>
                  <option value="md">Medium</option>
                  <option value="lg">Large</option>
                  <option value="xl">Extra Large</option>
                </select>
              </div>
            </>
          );
        case "contact_form":
          return (
            <>
              <div className="mb-4">
                <label className="block text-theme-secondary mb-2">Background Color</label>
                <input
                  type="text"
                  value={config.background_color || ""}
                  onChange={(e) => setConfig({ ...config, background_color: e.target.value })}
                  className="w-full px-3 py-2 border border-theme-secondary rounded"
                />
              </div>
              <div className="mb-4">
                <label className="block text-theme-secondary mb-2">Text Color</label>
                <input
                  type="text"
                  value={config.text_color || ""}
                  onChange={(e) => setConfig({ ...config, text_color: e.target.value })}
                  className="w-full px-3 py-2 border border-theme-secondary rounded"
                />
              </div>
              <div className="mb-4">
                <label className="block text-theme-secondary mb-2">Contact Form ID</label>
                <input
                  type="number"
                  value={config.contact_form_id || ""}
                  onChange={(e) => setConfig({ ...config, contact_form_id: e.target.value })}
                  className="w-full px-3 py-2 border border-theme-secondary rounded"
                />
              </div>
            </>
          );
        default:
          return <p className="text-theme-secondary">Configure block settings here.</p>;
      }
    };

    return (
      <div className="bg-card p-4 rounded-lg shadow">
        <h3 className="text-xl font-bold mb-4 text-theme">Edit {blockTypes[block.block_type]?.name || "Block"}</h3>
        
        <div className="mb-4">
          <label className="block text-theme-secondary mb-2">Title</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 border border-theme-secondary rounded"
          />
        </div>
        
        <div className="mb-4">
          <label className="block text-theme-secondary mb-2">Content</label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="w-full px-3 py-2 border border-theme-secondary rounded"
            rows="4"
          ></textarea>
        </div>
        
        <h4 className="font-bold mb-2 text-theme">Configuration</h4>
        {renderConfigOptions()}
        
        <div className="flex justify-between mt-6">
          <button
            onClick={() => setSelectedBlock(null)}
            className="bg-card text-theme px-4 py-2 rounded border border-theme"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="bg-primary hover:bg-primary-hover text-white px-4 py-2 rounded"
          >
            Save Block
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {/* Block List */}
      <div className="md:col-span-2">
        <div className="bg-card p-4 rounded-lg shadow editor-panel">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold text-theme">Homepage Blocks</h2>
            <button
              onClick={() => setAddingBlock(!addingBlock)}
              className="bg-primary hover:bg-primary-hover text-white px-4 py-2 rounded"
            >
              {addingBlock ? "Cancel" : "Add Block"}
            </button>
          </div>

          {/* Add Block Form */}
          {addingBlock && (
            <div className="mb-6 p-4 border border-theme-secondary rounded">
              <h3 className="text-lg font-bold mb-3 text-theme">Add New Block</h3>
              <div className="mb-4">
                <label className="block text-theme-secondary mb-2">Block Type</label>
                <select
                  value={newBlockType}
                  onChange={(e) => setNewBlockType(e.target.value)}
                  className="w-full px-3 py-2 border border-theme-secondary rounded"
                >
                  <option value="">Select a block type</option>
                  {Object.entries(blockTypes).map(([key, { name, icon }]) => (
                    <option key={key} value={key}>
                      {icon} {name}
                    </option>
                  ))}
                </select>
              </div>
              <button
                onClick={handleAddBlock}
                disabled={!newBlockType || loading}
                className="bg-primary hover:bg-primary-hover text-white px-4 py-2 rounded disabled:opacity-50"
              >
                {loading ? "Adding..." : "Add Block"}
              </button>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
              {error}
            </div>
          )}

          {/* Block List */}
          {blocks.length === 0 ? (
            <div className="text-center py-8 text-theme-secondary">
              No blocks added yet. Click "Add Block" to create your homepage.
            </div>
          ) : (
            <DragDropContext onDragEnd={handleDragEnd}>
              <Droppable droppableId="blocks">
                {(provided) => (
                  <div
                    {...provided.droppableProps}
                    ref={provided.innerRef}
                    className="space-y-3"
                  >
                    {blocks.map((block, index) => (
                      <Draggable
                        key={block.id.toString()}
                        draggableId={block.id.toString()}
                        index={index}
                      >
                        {(provided) => (
                          <div
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            className="bg-theme border border-theme-secondary rounded p-3 flex items-center justify-between"
                          >
                            <div className="flex items-center">
                              <span className="mr-3 text-xl">
                                {blockTypes[block.block_type]?.icon || "📦"}
                              </span>
                              <div>
                                <h3 className="font-medium text-theme">
                                  {block.title || blockTypes[block.block_type]?.name || "Block"}
                                </h3>
                                <p className="text-sm text-theme-secondary">
                                  {blockTypes[block.block_type]?.name || block.block_type}
                                </p>
                              </div>
                            </div>
                            <div className="flex items-center space-x-2">
                              <label className="inline-flex items-center cursor-pointer">
                                <input
                                  type="checkbox"
                                  checked={block.is_active}
                                  onChange={() =>
                                    handleUpdateBlock(block.id, {
                                      is_active: !block.is_active,
                                    })
                                  }
                                  className="form-checkbox h-5 w-5 text-primary"
                                />
                                <span className="ml-2 text-sm text-theme-secondary">
                                  Active
                                </span>
                              </label>
                              <button
                                onClick={() => setSelectedBlock(block)}
                                className="text-primary hover:text-primary-hover"
                              >
                                Edit
                              </button>
                              <button
                                onClick={() => handleDeleteBlock(block.id)}
                                className="text-red-500 hover:text-red-700"
                              >
                                Delete
                              </button>
                            </div>
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
      <div className="md:col-span-1">
        <div className="bg-card p-4 rounded-lg shadow editor-panel">
          {selectedBlock ? (
            <BlockEditor block={selectedBlock} />
          ) : (
            <div className="text-center py-8 text-theme-secondary">
              <p className="mb-4">Select a block to edit its content and settings.</p>
              <p>Or add a new block to get started.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Render the component
ReactDOM.render(<HomepageBuilder />, document.getElementById("homepage-builder"));