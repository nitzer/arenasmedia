// Copyright 2009 Martin Schuhfuss
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, 
// either express or implied. See the License for the specific
// language governing permissions and limitations under the License. 

/**
 * jQuery-tooltip extension.
 *
 * @plugin jquery.jtooltip
 * @provides jQuery.fn.tooltip()
 * 
 * @version 1.0
 * 
 * @require jQuery >= 1.2
 * @require jquery.hoverIntent.js <http://cherne.net/brian/resources/jquery.hoverIntent.html>
 * 
 * @author Martin Schuhfuss <m.schuhfuss@googlemail.com>
 */
;(function($) {
	$.tooltip = {
		//{{{ globals and default-settings
		/**
		 * @static  id of the div-container that holds the tooltip contents. Two
		 * additional conatiners with the ids <containerId>_wrap and
		 * <containerId>_shadow will be created in _createHelpers()
		 */
		containerId : 'tooltip',
		
		// instance-specific settings and default-values
		defaults: {
			/**
			 * @cfg {String|jQuery|Function} contents
			 *   html-string, jQuery-Object or a function that is called to
			 *   generate the contents for the element. If set, an existing
			 *   title-attribute will be ignored.
			 * 
			 * If a function is specified as argument, it is called with the
			 * event that triggered the tooltip as argument and is executed in
			 * the scope of the owner-element. It must return the contents as
			 * String, jQuery-Object or DOM-Element.
			 */
			contents : null,
			
			/**
			 * @cfg {String} extraClass
			 *   an extra css-class to be added to the tooltip's
			 *   content-container.
			 */
			extraClass : null,
			
			/**
			 * @cfg {int} maxWidth
			 *   maximum width of the wrapper-div
			 */
			maxWidth : 250,
			
			/**
			 * @cfg {int} posOffsetX
			 *   offset of the tooltip from Mouseposition
			 */
			posOffsetX : 3,
			
			/**
			 * @cfg {int} posOffsetY
			 *   offset of the tooltip from Mouseposition
			 */
			posOffsetY : 3,
			
			// hoverIntent-settings
			// NOTE: this plugin actually requires hoveIntent to work, therefore
			// there is no option to disable hoverIntent.
			/**
			 * @cfg {int} sensitivity
			 *   An amount of pixels the mouse might move within the given
			 *   interval without being recognized as an actual movement.
			 *
			 * @cfg {int} interval
			 *   The time (milliseconds) beetween two mouse-coordinate
			 *   evaluations. If the mouse stands still (see sensitivity) for
			 *   this amount of time the tooltip is activated.
			 *
			 * @cfg {int} timeout
			 *   The timeout beetween the leaving of the tooltip-area and the
			 *   closing of the tooltip. Reentering the tooltip within this
			 *   period cancels the timeout.
			 */
			sensitivity: 10,
			interval: 200,
			timeout: 100
		},
		//}}}
	};
	
	// jQuery plugin-methods
	$.fn.extend({
		//{{{ tooltip(settings)
		/**
		 * adds tooltip-behaviour to a jQuery-Object (representing a single or a set of elements)
		 *
		 * @scope jQuery
		 * @param {any} p 
		 *    the tooltip-text, a jQuery-Object that holds the tooltip contents, a function
		 *    to return the contents or a setings-object. See above for a list of possible
		 *    settings.
		 *
		 * @return the jQuery-Object on which this method was called.
		 */
		tooltip: function(p) {
			settings = $.extend({}, $.tooltip.defaults);
		  if(p instanceof jQuery || typeof p !== 'object') {
				$.extend(settings, {contents : p});
			} else {
				$.extend(settings, p);
			}
			
			settings.over = _show;
			settings.out = _hide;
			
			// setup helpers.
			if(helpers === null) { _createHelpers(settings); }
			
			return this.data('tooltipSettings', settings)
				.each(_initTooltipDataForElement)
				.hoverIntent(settings)
				.bind('mouseover.tracking mouseout.tracking', _toggleTracking);
		}
		//}}}
	});
	//}}}
	
	//{{{ private members
	/**
	 * container-object for helper-elements. These are:
	 *   helpers.wrap: container for all elements
	 *   helpers.ct: content-Container
	 *   helpers.shadow: shadow-div
	 *
	 * @var {Object}
	 */
	var helpers = null;
	
	/**
	 * current mouse-position used to position the tooltip.
	 * @var {int}
	 */
	var mX, mY;
	
	//{{{ _initTooltipDataForElement()
	/**
	 * initialize the tooltip for a dom-element.
	 *
	 * @param {Object} settings  the settings for this tooltip.
	 * @scope {DomElement}
	 */
	function _initTooltipDataForElement() {
		var settings = $(this).data('tooltipSettings');
		// copy tooltip into its own expando and remove the title
		this.tooltipText = this.title;
		// remove title and alt attributes to prevent default tooltips
		$(this)
				.removeAttr('title')
				.removeAttr('alt');
	};
	//}}}
	
	//{{{ _createHelpers(settings)
	/**
	 * creates the helper-elements, that is the dom-elements required to show
	 * the tooltips.
	 */
	function _createHelpers(settings) {
		var cId = $.tooltip.containerId;
		helpers = {};
		helpers.wrap = $(
			  '<div id="' + cId + '_wrap">'
			+   '<div id="' + cId + '"></div>'
			+   '<div id="' + cId + '_shadow" ></div>'
			+ '</div>'
		).css({width : settings.maxWidth + 'px'}).appendTo('body').hide();
		
		helpers.ct = $('#' + cId, helpers.wrap);
		helpers.shadow = $('#' + cId + '_shadow', helpers.wrap);
	};
	//}}}
	
	//{{{ _show(ev)
	/**
	 * @scope {DomElement}      the element for which the tooltip should be shown
	 * @param {EventObject} ev  the event
	 */
	function _show(ev) {
		var s=$(this).data('tooltipSettings');
		
		_updateHelpers(this, ev, s);
		
		_positionAndResizeHelpers(s);
		// mouseover and -out events for the tooltip must be delegated to the
		// element that holds the tooltip. Therefor we need to swap the target
		// and relatedTarget/fromElement/toElement-properties.
		var holder = this;
		
		helpers.wrap.bind( 'mouseover mouseout', function(e) {
			var tmp = (e.type == "mouseover" ? e.fromElement : e.toElement) || e.relatedTarget;
			e.relatedTarget = e.target;
			e.target = tmp;
			
			$(holder).triggerHandler(e.type, e);
		});
		
		// show container
		helpers.wrap.show();
		return false;
	};
	//}}}
	
	//{{{ _hide(ev)
	/**
	 * @scope DOMElement  the element for which
	 * @param EventObject  the event
	 */
	function _hide(ev) {
		if(!helpers.wrap.is(":visible")) {
			return;
		}
		
		helpers.wrap.hide();
		helpers.wrap.unbind('mouseover mouseout');
	};
	//}}}
	
	//{{{ _updateHelpers(dom, ev, s)
	/**
	 * updates the helpers before shown.
	 *
	 * @param  {DomElement} dom  the element for which the tooltip should be shown
	 * @param  {EventObject} ev  the mouseover-event as it was relayed by hoverIntent
	 * @param  {Object} s        the settings-object for the tooltip
	 */
	function _updateHelpers(dom, ev, s) {
		var contents = dom.tooltipText;
		if(s.contents !== null) {
			if(typeof s.contents === 'function') {
				contents = s.contents.call(dom, ev, s);
			} else {
				contents = s.contents;
			}
		}
		
		helpers.ct.empty().append(contents);
		helpers.ct.removeClass();
		
		if(s.extraClass !== null) { helpers.ct.addClass(s.extraClass); }
	};
	//}}}
	
	//{{{ _positionAndResizeHelpers(s)
	function _positionAndResizeHelpers(s) {
		var screenWidth = $(window).width(),
				screenHeight = $(window).height(),
				ttLeft = mX + s.posOffsetX,
				ttTop = mY + s.posOffsetY;
		
		// read out content's width and height
		helpers.wrap.css({
			visibility: 'hidden',
			display: 'block',
			width: '100%'
		});
		helpers.ct.css({ width: 'auto', height: 'auto'});
		var ctWidth = helpers.ct.outerWidth(),
			ctHeight = helpers.ct.outerHeight();
		
		// update width and height if contents are too wide
		if(ctWidth > s.maxWidth) {
			ctWidth = s.maxWidth;
			
			helpers.ct.css({width: ctWidth });
			ctHeight = helpers.ct.outerHeight();
		}
		
		helpers.wrap.css({
			display: 'none', visibility: 'visible',
			left: ttLeft,
			top: ttTop,
			width: ctWidth
		});
		
		// check if tooltip will fit into the viewport, reposition if not
		if(screenWidth < ttLeft + ctWidth + 5) {
			helpers.wrap.css({
				left: mX - s.posOffsetX - ctWidth
			});
		}
		
		if(screenHeight < ttTop + ctHeight + 5) {
			helpers.wrap.css({
				top: mY - s.posOffsetY - ctHeight
			});
		}
		
		// update geometry of shadow and wrapper.
		helpers.shadow.css({width:ctWidth, height:ctHeight});
		helpers.wrap.css({width:ctWidth});
	}
	//}}}
	
	//{{{ _toggleTracking(ev)
	function _toggleTracking(ev) {
		if(ev.type === 'mouseover') {
			$(this).bind('mousemove.tracking', _trackMouse );
		} else {
			$(this).unbind('mousemove.tracking');
		}
	};
	//}}}
	//{{{ _trackMouse(e)
	function _trackMouse(e) {
		mX=e.pageX;
		mY=e.pageY;
	};
	//}}}
	//}}}
})(jQuery);
// vim: ts=2 sw=2 foldmethod=marker noexpandtab
