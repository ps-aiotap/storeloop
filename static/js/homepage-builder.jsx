import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

// Block Type Components
const BlockTypeLibrary = ({ blockTypes, onAddBlock }) => {
  return (
    <div className="block-library">
      <h2 className="text-xl font-bold text-theme mb-4">Block Library</h2>
      <div className="space-y-3">
        {blockTypes.map((blockType) => (
          <div
            key={blockType.type}
            className="block-library-item bg-theme p-3 rounded border border-theme cursor-pointer hover:shadow-md transition-transform hover:-translate-y-1"
            onClick={() => onAddBlock(blockType.type, blockType.name)}
          >
            <h3 className="font-medium text-theme">{blockType.name}</h3>
            <p className="text-sm text-theme-secondary">{blockType.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

// Block List Component
const BlockList = ({ blocks, onSelectBlock, onToggleActive, onDeleteBlock, selectedBlockId }) => {
  const getBlockTypeName = (blockType) => {
    const blockTypeMap = {
      'hero_banner': 'Hero Banner',
      'product_grid': 'Product Grid',
      'featured_products': 'Featured Products',
      'testimonials': 'Testimonials',
      'text_block': 'Text Block',
      'image_gallery': 'Image Gallery',
      'newsletter_signup': 'Newsletter Signup',
      'video_embed': 'Video Embed'
    };
    return blockTypeMap[blockType] || blockType;
  };

  return (
    <DragDropContext onDragEnd={(result) => console.log(result)}>
      <Droppable droppableId="blocks-list">
        {(provided) => (
          <div
            ref={provided.innerRef}
            {...provided.droppableProps}
            className="space-y-3"
          >
            {blocks.length === 0 ? (
              <div className="text-center py-8 border-2 border-dashed border-theme-secondary rounded-lg">
                <p className="text-theme-secondary">Drag blocks from the library to build your homepage</p>
              </div>
            ) : (
              blocks.map((block, index) => (
                <Draggable key={block.id} draggableId={`block-${block.id}`} index={index}>
                  {(provided) => (
                    <div
                      ref={provided.innerRef}
                      {...provided.draggableProps}
                      {...provided.dragHandleProps}
                      className={`block-item bg-theme p-3 rounded border ${
                        selectedBlockId === block.id ? 'border-primary' : 'border-theme'
                      }`}
                    >
                      <div className="flex justify-between items-center">
                        <div className="flex items-center">
                          <span className="mr-2 text-theme-secondary">{index + 1}</span>
                          <h3 className="font-medium text-theme">
                            {block.title || getBlockTypeName(block.block_type)}
                          </h3>
                        </div>
                        <div className="flex space-x-2">
                          <button
                            onClick={() => onToggleActive(block)}
                            className="p-1 rounded hover:bg-theme-secondary"
                          >
                            <span className={block.is_active ? 'text-green-500' : 'text-red-500'}>
                              {block.is_active ? '●' : '○'}
                            </span>
                          </button>
                          <button
                            onClick={() => onSelectBlock(block)}
                            className="p-1 rounded hover:bg-theme-secondary"
                          >
                            <span className="text-theme">✎</span>
                          </button>
                          <button
                            onClick={() => onDeleteBlock(block)}
                            className="p-1 rounded hover:bg-theme-secondary"
                          >
                            <span className="text-red-500">✕</span>
                          </button>
                        </div>
                      </div>
                    </div>
                  )}
                </Draggable>
              ))
            )}
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </DragDropContext>
  );
};

// Block Configuration Component
const BlockConfiguration = ({ selectedBlock, onUpdateBlock }) => {
  const [blockData, setBlockData] = useState(selectedBlock);

  useEffect(() => {
    setBlockData(selectedBlock);
  }, [selectedBlock]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setBlockData({
      ...blockData,
      [name]: value
    });
  };

  const handleConfigChange = (e) => {
    const { name, value } = e.target;
    setBlockData({
      ...blockData,
      configuration: {
        ...blockData.configuration,
        [name]: value
      }
    });
  };

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setBlockData({
      ...blockData,
      configuration: {
        ...blockData.configuration,
        [name]: checked
      }
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onUpdateBlock(blockData);
  };

  const getBlockTypeName = (blockType) => {
    const blockTypeMap = {
      'hero_banner': 'Hero Banner',
      'product_grid': 'Product Grid',
      'featured_products': 'Featured Products',
      'testimonials': 'Testimonials',
      'text_block': 'Text Block',
      'image_gallery': 'Image Gallery',
      'newsletter_signup': 'Newsletter Signup',
      'video_embed': 'Video Embed'
    };
    return blockTypeMap[blockType] || blockType;
  };

  if (!selectedBlock) {
    return (
      <div className="text-center py-8">
        <p className="text-theme-secondary">Select a block to configure</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className="mb-4">
        <label className="block text-theme-secondary mb-1">Block Type</label>
        <div className="font-medium text-theme">{getBlockTypeName(blockData.block_type)}</div>
      </div>

      <div className="mb-4">
        <label htmlFor="title" className="block text-theme-secondary mb-1">Title</label>
        <input
          type="text"
          id="title"
          name="title"
          value={blockData.title}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-theme-secondary rounded bg-theme text-theme"
        />
      </div>

      {['text_block', 'testimonials'].includes(blockData.block_type) && (
        <div className="mb-4">
          <label htmlFor="content" className="block text-theme-secondary mb-1">Content</label>
          <textarea
            id="content"
            name="content"
            value={blockData.content}
            onChange={handleChange}
            rows="4"
            className="w-full px-3 py-2 border border-theme-secondary rounded bg-theme text-theme"
          ></textarea>
        </div>
      )}

      {/* Hero Banner Configuration */}
      {blockData.block_type === 'hero_banner' && (
        <div className="space-y-4">
          <div>
            <label htmlFor="image_url" className="block text-theme-secondary mb-1">Image URL</label>
            <input
              type="text"
              id="image_url"
              name="image_url"
              value={blockData.configuration.image_url || ''}
              onChange={handleConfigChange}
              className="w-full px-3 py-2 border border-theme-secondary rounded bg-theme text-theme"
            />
          </div>
          <div>
            <label htmlFor="button_text" className="block text-theme-secondary mb-1">Button Text</label>
            <input
              type="text"
              id="button_text"
              name="button_text"
              value={blockData.configuration.button_text || ''}
              onChange={handleConfigChange}
              className="w-full px-3 py-2 border border-theme-secondary rounded bg-theme text-theme"
            />
          </div>
          <div>
            <label htmlFor="button_url" className="block text-theme-secondary mb-1">Button URL</label>
            <input
              type="text"
              id="button_url"
              name="button_url"
              value={blockData.configuration.button_url || ''}
              onChange={handleConfigChange}
              className="w-full px-3 py-2 border border-theme-secondary rounded bg-theme text-theme"
            />
          </div>
          <div>
            <label htmlFor="height" className="block text-theme-secondary mb-1">Height</label>
            <select
              id="height"
              name="height"
              value={blockData.configuration.height || 'lg'}
              onChange={handleConfigChange}
              className="w-full px-3 py-2 border border-theme-secondary rounded bg-theme text-theme"
            >
              <option value="sm">Small</option>
              <option value="md">Medium</option>
              <option value="lg">Large</option>
              <option value="xl">Extra Large</option>
            </select>
          </div>
        </div>
      )}

      {/* Product Grid Configuration */}
      {blockData.block_type === 'product_grid' && (
        <div className="space-y-4">
          <div>
            <label htmlFor="products_count" className="block text-theme-secondary mb-1">Number of Products</label>
            <input
              type="number"
              id="products_count"
              name="products_count"
              value={blockData.configuration.products_count || 6}
              onChange={handleConfigChange}
              className="w-full px-3 py-2 border border-theme-secondary rounded bg-theme text-theme"
            />
          </div>
          <div>
            <label htmlFor="columns" className="block text-theme-secondary mb-1">Columns</label>
            <select
              id="columns"
              name="columns"
              value={blockData.configuration.columns || 3}
              onChange={handleConfigChange}
              className="w-full px-3 py-2 border border-theme-secondary rounded bg-theme text-theme"
            >
              <option value="2">2 Columns</option>
              <option value="3">3 Columns</option>
              <option value="4">4 Columns</option>
            </select>
          </div>
          <div className="flex items-center">
            <input
              type="checkbox"
              id="show_price"
              name="show_price"
              checked={blockData.configuration.show_price !== false}
              onChange={handleCheckboxChange}
            />
            <label htmlFor="show_price" className="ml-2 text-theme">Show Price</label>
          </div>
          <div className="flex items-center">
            <input
              type="checkbox"
              id="show_description"
              name="show_description"
              checked={blockData.configuration.show_description === true}
              onChange={handleCheckboxChange}
            />
            <label htmlFor="show_description" className="ml-2 text-theme">Show Description</label>
          </div>
          <div className="flex items-center">
            <input
              type="checkbox"
              id="show_view_all"
              name="show_view_all"
              checked={blockData.configuration.show_view_all === true}
              onChange={handleCheckboxChange}
            />
            <label htmlFor="show_view_all" className="ml-2 text-theme">Show "View All" Button</label>
          </div>
        </div>
      )}

      <div className="mt-6">
        <button
          type="submit"
          className="w-full bg-primary hover:bg-primary-hover text-white px-4 py-2 rounded"
        >
          Update Block
        </button>
      </div>
    </form>
  );
};

// Main Homepage Builder Component
const HomepageBuilder = () => {
  const [blocks, setBlocks] = useState([]);
  const [selectedBlock, setSelectedBlock] = useState(null);
  const [selectedBlockId, setSelectedBlockId] = useState(null);
  const [blockTypes, setBlockTypes] = useState([
    { type: 'hero_banner', name: 'Hero Banner', description: 'Large banner with image and call-to-action' },
    { type: 'product_grid', name: 'Product Grid', description: 'Display products in a grid layout' },
    { type: 'featured_products', name: 'Featured Products', description: 'Showcase featured or bestselling products' },
    { type: 'testimonials', name: 'Testimonials', description: 'Customer reviews and testimonials' },
    { type: 'text_block', name: 'Text Block', description: 'Rich text content area' },
    { type: 'image_gallery', name: 'Image Gallery', description: 'Multiple images in a gallery layout' },
    { type: 'newsletter_signup', name: 'Newsletter Signup', description: 'Email subscription form' },
    { type: 'video_embed', name: 'Video Embed', description: 'Embed video content' }
  ]);

  // Load initial blocks from the server
  useEffect(() => {
    // Get blocks from the data attribute
    const blocksContainer = document.getElementById('homepage-builder');
    if (blocksContainer) {
      try {
        const initialBlocks = JSON.parse(blocksContainer.dataset.blocks || '[]');
        setBlocks(initialBlocks);
      } catch (e) {
        console.error('Error parsing initial blocks:', e);
      }
    }
  }, []);

  const addNewBlock = (blockType, blockName) => {
    // Get CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    // Send request to create new block
    fetch(`/stores/${window.storeSlug}/homepage/blocks/create/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
        block_type: blockType,
        title: blockName
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        const newBlock = {
          id: data.block_id,
          block_type: data.block_type,
          title: data.title,
          content: '',
          order: data.order,
          is_active: true,
          configuration: getDefaultConfiguration(data.block_type)
        };
        
        setBlocks([...blocks, newBlock]);
        selectBlock(newBlock);
      }
    })
    .catch(error => {
      console.error('Error creating block:', error);
    });
  };

  const selectBlock = (block) => {
    setSelectedBlock(JSON.parse(JSON.stringify(block))); // Clone to avoid direct reference
    setSelectedBlockId(block.id);
  };

  const updateBlock = (updatedBlock) => {
    // Update local state
    const updatedBlocks = blocks.map(block => 
      block.id === updatedBlock.id ? updatedBlock : block
    );
    setBlocks(updatedBlocks);
    setSelectedBlock(updatedBlock);
    
    // Send update to server
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(`/stores/${window.storeSlug}/homepage/blocks/${updatedBlock.id}/update/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify(updatedBlock)
    })
    .catch(error => {
      console.error('Error updating block:', error);
    });
  };

  const deleteBlock = (block) => {
    if (!confirm('Are you sure you want to delete this block?')) return;
    
    // Remove from local state
    setBlocks(blocks.filter(b => b.id !== block.id));
    
    // Clear selection if needed
    if (selectedBlockId === block.id) {
      setSelectedBlock(null);
      setSelectedBlockId(null);
    }
    
    // Send delete request to server
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(`/stores/${window.storeSlug}/homepage/blocks/${block.id}/delete/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      }
    })
    .catch(error => {
      console.error('Error deleting block:', error);
    });
  };

  const toggleBlockActive = (block) => {
    const updatedBlock = {
      ...block,
      is_active: !block.is_active
    };
    
    // Update local state
    const updatedBlocks = blocks.map(b => 
      b.id === block.id ? updatedBlock : b
    );
    setBlocks(updatedBlocks);
    
    // If this is the selected block, update selection
    if (selectedBlockId === block.id) {
      setSelectedBlock(updatedBlock);
    }
    
    // Send update to server
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(`/stores/${window.storeSlug}/homepage/blocks/${block.id}/update/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
        is_active: updatedBlock.is_active
      })
    })
    .catch(error => {
      console.error('Error updating block:', error);
    });
  };

  const getDefaultConfiguration = (blockType) => {
    switch(blockType) {
      case 'hero_banner':
        return {
          image_url: '',
          button_text: 'Shop Now',
          button_url: '/products/',
          height: 'lg',
          overlay_opacity: 50,
          text_color: 'white'
        };
      case 'product_grid':
        return {
          products_count: 6,
          columns: 3,
          show_price: true,
          show_description: false,
          show_view_all: true,
          sort_by: 'newest'
        };
      case 'testimonials':
        return {
          style: 'cards',
          testimonials: [
            {
              name: 'Customer Name',
              role: 'Customer',
              content: 'This is a great product!',
              image_url: ''
            }
          ]
        };
      case 'text_block':
        return {
          alignment: 'left',
          max_width: 'lg',
          background_color: '',
          text_color: ''
        };
      default:
        return {};
    }
  };

  return (
    <div className="homepage-builder">
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Block Library */}
        <div className="lg:col-span-1 bg-card p-4 rounded-lg shadow editor-panel">
          <BlockTypeLibrary blockTypes={blockTypes} onAddBlock={addNewBlock} />
        </div>
        
        {/* Block Editor */}
        <div className="lg:col-span-2 bg-card p-4 rounded-lg shadow editor-panel">
          <h2 className="text-xl font-bold text-theme mb-4">Homepage Layout</h2>
          <BlockList
            blocks={blocks}
            onSelectBlock={selectBlock}
            onToggleActive={toggleBlockActive}
            onDeleteBlock={deleteBlock}
            selectedBlockId={selectedBlockId}
          />
        </div>
        
        {/* Block Configuration */}
        <div className="lg:col-span-1 bg-card p-4 rounded-lg shadow editor-panel">
          <h2 className="text-xl font-bold text-theme mb-4">Block Configuration</h2>
          <BlockConfiguration
            selectedBlock={selectedBlock}
            onUpdateBlock={updateBlock}
          />
        </div>
      </div>
    </div>
  );
};

// Initialize React app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  const container = document.getElementById('homepage-builder');
  if (container) {
    ReactDOM.render(<HomepageBuilder />, container);
  }
});