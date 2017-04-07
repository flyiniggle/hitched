(function($) {
    "use strict"; // Start of use strict

    // jQuery for page scrolling feature - requires jQuery Easing plugin
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($anchor.attr('href')).offset().top - 50)
        }, 900, 'easeOutCubic');
        event.preventDefault();
    });

    // Highlight the top nav as scrolling occurs
    $('body').scrollspy({
        target: '.navbar-fixed-top',
        offset: 51
    });

    // Closes the Responsive Menu on Menu Item Click
    $('.navbar-collapse ul li a').click(function() {
        $('.navbar-toggle:visible').click();
    });

    // Offset for Main Navigation
    $('#mainNav').affix({
        offset: {
            top: 100
        }
    })

    // Initialize and Configure Scroll Reveal Animation
    window.sr = ScrollReveal();
    sr.reveal('.sr-icons', {
        duration: 600,
        scale: 0.3,
        distance: '0px'
    }, 200);
    sr.reveal('.sr-button', {
        duration: 1000,
        delay: 200
    });
    sr.reveal('.sr-contact', {
        duration: 600,
        scale: 0.3,
        distance: '0px'
    }, 300);

    // Initialize and Configure Magnific Popup Lightbox Plugin
    $('.popup-gallery').magnificPopup({
        delegate: 'a',
        type: 'image',
        tLoading: 'Loading image #%curr%...',
        mainClass: 'mfp-img-mobile',
        gallery: {
            enabled: true,
            navigateByImgClick: true,
            preload: [0, 1] // Will preload 0 - before current, and 1 after the current image
        },
        image: {
            tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
        }
    });

    function RSVPModel() {
		var self = this;

        self.name = ko.observable("");
        self.address = ko.observable("");
        self.guests = ko.observableArray([]);
		self.invitations = ko.observableArray([]);
		self.selectedInvitation = ko.observable();
        self.enableLookup = ko.computed(function() {
            if (self.name()) {
                return self.name();
            } else if (self.address()) {
                return self.address();
            } else {
                return false;
            }
        }).extend({throttle: 750});

		this.address.subscribe(function() {
			self.guests([]);
			self.invitations([]);
		});
		this.name.subscribe(function() {
			self.guests([]);
			self.invitations([]);
		});

        this.enableLookup.subscribe(function() {
            var url, data;

			self.guests([]);
			self.invitations([]);
            if (self.name() === "" && self.address() === "") {
                return;
            }

            url = self.name() ? "/guest_name" : "/guest_address";
            data = self.name() ? {name: encodeURIComponent(self.name().trim().toLowerCase())} : {address: encodeURIComponent(self.address().trim().toLowerCase())};

            $.get(url, data, function(result) {
            	var responseJSON = JSON.parse(result);

				self.guests([]);
				self.invitations([]);
				if(responseJSON.error) {
					return;
				}

				if(responseJSON.length && responseJSON.length > 1) {
					responseJSON.forEach(function(invitation) {
						self.invitations.push(new InvitationOption(invitation));
					});
				} else if (responseJSON.Guests) {
					responseJSON.Guests.forEach(function(guest) {
						self.guests.push(new GuestModel(guest.Name));
					});
					if(responseJSON["Plus One"] === true) {
						self.guests.push(new GuestModel());
					}
				}
            });
        });

		this.swapInput = function() {
			if(!!self.name()) {
				self.name("");
				self.address(self.selectedInvitation());
			} else {
				self.address("");
				self.name(self.selectedInvitation());
			}
		}
    }

    function GuestModel(name) {
        var guestName = name || "";

        this.name = ko.observable(guestName);
		this.isPlusOne = !name;
        this.isComing = ko.observable(!!guestName);
        this.isVegetarain = ko.observable(false);
    }

	function InvitationOption(invitation) {
		this.address = invitation.Address;
		this.name = invitation.Name;
	}

    ko.applyBindings(new RSVPModel());

})(jQuery); // End of use strict
