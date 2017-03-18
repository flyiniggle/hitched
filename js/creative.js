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
        this.name = ko.observable("");
        this.address = ko.observable("");
        this.guests = ko.observableArray([]);
        this.isCamping = ko.observable(false);
        this.regrets = ko.observable(false);
        this.enableLookup = ko.computed(function() {
            if (this.name()) {
                return this.name();
            } else if (this.address()) {
                return this.address();
            } else {
                return false;
            }
        }.bind(this)).extend({throttle: 750});

        this.enableLookup.subscribe(function() {
            var url, data;

            if (this.name() === "" && this.address() === "") {
                return;
            }

            url = this.name() ? "/guest_name" : "/guest_address";
            data = this.name() ? {name: encodeURIComponent(this.name())} : {address: encodeURIComponent(this.address())};

            $.get(url, data, function(result) {
                console.log(result);
            });
        }.bind(this));
    }

    function GuestModel(name) {
        var guestName = name || "";

        this.name = ko.observable(guestName);
        this.isVegetarain = ko.observable(false);
    }

    ko.applyBindings(new RSVPModel());

})(jQuery); // End of use strict
